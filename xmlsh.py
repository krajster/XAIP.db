#!/usr/bin/python
# Script created by Isox 18.11.2011
# Update 21.11.2011 : Added etree lib for preserver attributes order.
# Update 22.11.2011 : Removed minidom. All parsing made on etree. Added "add", "settext" commands. Improved "cd".
#
# This XMLsh utility will help you to agregate state.db file
# With best regards.
from subprocess import call
try:
    import xml.etree.ElementTree as etree
except:
    import elementtree.ElementTree as etree
import sys
ver=list(sys.version.split())[0]
try:
    from thread import get_ident as _get_ident
except:
    from collections import OrderedDict as odict
else:
    class _Nil(object):
        def __repr__(self):
            return "nil"

        def __eq__(self, other):
            if (isinstance(other, _Nil)):
                return True
            else:
                return NotImplemented

        def __ne__(self, other):
            if (isinstance(other, _Nil)):
                return False
            else:
                return NotImplemented

    _nil = _Nil()

    class _odict(object):
        def _dict_impl(self):
            return None

        def __init__(self, data=(), **kwds):
            if kwds:
                raise TypeError(" ")
            self._dict_impl().__init__(self)
        # If you give a normal dict, then the order of elements is undefined
            if hasattr(data, "iteritems"):
                for key, val in data.iteritems():
                    self[key] = val
            else:
                for key, val in data:
                    self[key] = val

        # Double-linked list header
        def _get_lh(self):
            dict_impl = self._dict_impl()
            if not hasattr(self, '_lh'):
                dict_impl.__setattr__(self, '_lh', _nil)
            return dict_impl.__getattribute__(self, '_lh')

        def _set_lh(self, val):
            self._dict_impl().__setattr__(self, '_lh', val)

        lh = property(_get_lh, _set_lh)

        # Double-linked list tail
        def _get_lt(self):
            dict_impl = self._dict_impl()
            if not hasattr(self, '_lt'):
                dict_impl.__setattr__(self, '_lt', _nil)
            return dict_impl.__getattribute__(self, '_lt')

        def _set_lt(self, val):
            self._dict_impl().__setattr__(self, '_lt', val)

        lt = property(_get_lt, _set_lt)

        def __getitem__(self, key):
            return self._dict_impl().__getitem__(self, key)[1]

        def __setitem__(self, key, val):
            dict_impl = self._dict_impl()
            try:
                dict_impl.__getitem__(self, key)[1] = val
            except KeyError:
                new = [dict_impl.__getattribute__(self, 'lt'), val, _nil]
                dict_impl.__setitem__(self, key, new)
                if dict_impl.__getattribute__(self, 'lt') == _nil:
                    dict_impl.__setattr__(self, 'lh', key)
                else:
                    dict_impl.__getitem__(
                        self, dict_impl.__getattribute__(self, 'lt'))[2] = key
                dict_impl.__setattr__(self, 'lt', key)

        def __delitem__(self, key):
            dict_impl = self._dict_impl()
            pred, _ ,succ= self._dict_impl().__getitem__(self, key)
            if pred == _nil:
                dict_impl.__setattr__(self, 'lh', succ)
            else:
                dict_impl.__getitem__(self, pred)[2] = succ
            if succ == _nil:
                dict_impl.__setattr__(self, 'lt', pred)
            else:
                dict_impl.__getitem__(self, succ)[0] = pred
            dict_impl.__delitem__(self, key)

        def __contains__(self, key):
            # XXX: try: self[key] ...
            return key in self.keys()

        def has_key(self, key):
            return key in self

        def __len__(self):
            return len(self.keys())

        def __str__(self):
            pairs = ("%r: %r" % (k, v) for k, v in self.iteritems())
            return "{%s}" % ", ".join(pairs)

        def __repr__(self):
            if self:
                pairs = ("(%r, %r)" % (k, v) for k, v in self.iteritems())
                return "odict([%s])" % ", ".join(pairs)
            else:
                return "odict()"

        def get(self, k, x=None):
            if k in self:
                return self._dict_impl().__getitem__(self, k)[1]
            else:
                return x

        def __iter__(self):
            dict_impl = self._dict_impl()
            curr_key = dict_impl.__getattribute__(self, 'lh')
            while curr_key != _nil:
                yield curr_key
                curr_key = dict_impl.__getitem__(self, curr_key)[2]

        iterkeys = __iter__

        def keys(self):
            return list(self.iterkeys())

        def itervalues(self):
            dict_impl = self._dict_impl()
            curr_key = dict_impl.__getattribute__(self, 'lh')
            while curr_key != _nil:
                _, val, curr_key = dict_impl.__getitem__(self, curr_key)
                yield val

        def values(self):
            return list(self.itervalues())

        def iteritems(self):
            dict_impl = self._dict_impl()
            curr_key = dict_impl.__getattribute__(self, 'lh')
            while curr_key != _nil:
                _, val, next_key = dict_impl.__getitem__(self, curr_key)
                yield curr_key, val
                curr_key = next_key

        def items(self):
            return list(self.iteritems())

        def sort(self, cmp=None, key=None, reverse=False):
            items = [(k, v) for k,v in self.items()]
            if cmp is not None:
                items = sorted(items, cmp=cmp)
            elif key is not None:
                items = sorted(items, key=key)
            else:
                items = sorted(items, key=lambda x: x[1])
            if reverse:
                items.reverse()
            self.clear()
            self.__init__(items)

        def clear(self):
            dict_impl = self._dict_impl()
            dict_impl.clear(self)
            dict_impl.__setattr__(self, 'lh', _nil)
            dict_impl.__setattr__(self, 'lt', _nil)

        def copy(self):
            return self.__class__(self)

        def update(self, data=(), **kwds):
            if kwds:
                raise TypeError("update() of ordered dict takes no keyword "
                                "arguments to avoid an ordering trap.")
            if hasattr(data, "iteritems"):
                data = data.iteritems()
            for key, val in data:
                self[key] = val

        def setdefault(self, k, x=None):
            try:
                return self[k]
            except KeyError:
                self[k] = x
                return x

        def pop(self, k, x=_nil):
            try:
                val = self[k]
                del self[k]
                return val
            except KeyError:
                if x == _nil:
                    raise
                return x

        def popitem(self):
            try:
                dict_impl = self._dict_impl()
                key = dict_impl.__getattribute__(self, 'lt')
                return key, self.pop(key)
            except KeyError:
                raise KeyError("'popitem(): ordered dictionary is empty'")

        def riterkeys(self):
            """To iterate on keys in reversed order.
            """
            dict_impl = self._dict_impl()
            curr_key = dict_impl.__getattribute__(self, 'lt')
            while curr_key != _nil:
                yield curr_key
                curr_key = dict_impl.__getitem__(self, curr_key)[0]

        __reversed__ = riterkeys

        def rkeys(self):
            """List of the keys in reversed order.
            """
            return list(self.riterkeys())

        def ritervalues(self):
            """To iterate on values in reversed order.
            """
            dict_impl = self._dict_impl()
            curr_key = dict_impl.__getattribute__(self, 'lt')
            while curr_key != _nil:
                curr_key, val, _ = dict_impl.__getitem__(self, curr_key)
                yield val

        def rvalues(self):
            """List of the values in reversed order.
            """
            return list(self.ritervalues())

        def riteritems(self):
            """To iterate on (key, value) in reversed order.
            """
            dict_impl = self._dict_impl()
            curr_key = dict_impl.__getattribute__(self, 'lt')
            while curr_key != _nil:
                pred_key, val, _ = dict_impl.__getitem__(self, curr_key)
                yield curr_key, val
                curr_key = pred_key

        def ritems(self):
            """List of the (key, value) in reversed order.
            """
            return list(self.riteritems())

        def firstkey(self):
            if self:
                return self._dict_impl().__getattribute__(self, 'lh')
            else:
                raise KeyError("'firstkey(): ordered dictionary is empty'")

        def lastkey(self):
            if self:
                return self._dict_impl().__getattribute__(self, 'lt')
            else:
                raise KeyError("'lastkey(): ordered dictionary is empty'")

        def as_dict(self):
            return self._dict_impl()(self.items())

        def _repr(self):
            """_repr(): low level repr of the whole data contained in the odict.
            Useful for debugging.
            """
            dict_impl = self._dict_impl()
            form = "odict low level repr lh,lt,data: %r, %r, %s"
            return form % (dict_impl.__getattribute__(self, 'lh'),
                           dict_impl.__getattribute__(self, 'lt'),
                           dict_impl.__repr__(self))

    class odict(_odict, dict):
        def _dict_impl(self):
            return dict

if(ver[0]=="3"):
#Ordered atributes tree building for Python 3
    def _start_list(self, tag, attrib_in):
        fixname = self._fixname
        tag = fixname(tag)
        attrib=odict()
        if attrib_in:
            for i in range(0, len(attrib_in), 2):
                attrib[fixname(attrib_in[i])] = attrib_in[i+1]
        return self.target.start(tag, attrib)
#Replace base function with mine
    etree.XMLTreeBuilder._start_list = _start_list
if(ver[0]=="2"):
#Ordered atributes tree building for Python 2.4
    def _start(self, tag, attrib_in):
        fixname = self._fixname
        tag = fixname(tag)
        attrib = odict()
        for key, value in attrib_in.items():
            attrib[fixname(key)] = self._fixtext(value)
        return self._target.start(tag, attrib)
    
    def _start_list(self, tag, attrib_in):
        fixname = self._fixname
        tag = fixname(tag)
        attrib = odict()
        if attrib_in:
            for i in range(0, len(attrib_in), 2):
                attrib[fixname(attrib_in[i])] = attrib_in[i+1]
        return self._target.start(tag, attrib)
#Replace base function with mine
    etree.XMLTreeBuilder._start_list = _start_list
    etree.XMLTreeBuilder._strt = _start
if(ver[0]=="3"):
#Ordered serializer....let's try =)
    def _serialize_xml(write, elem, qnames, namespaces):
        tag = elem.tag
        text = elem.text
        if tag is etree.Comment:
            write("<!--%s-->" % text)
        elif tag is etree.ProcessingInstruction:
            write("<?%s?>" % text)
        else:
            tag = qnames[tag]
            if tag is None:
                if text:
                    write(etree._escape_cdata(text))
                for e in elem:
                    etree._serialize_xml(write, e, qnames, None)
            else:
                write("<" + tag)
                items = list(elem.items())
                if items or namespaces:
                    if namespaces:
                        for v, k in sorted(namespaces.items(),
                                           key=lambda x: x[1]):  # sort on prefix
                            if k:
                                k = ":" + k
                            write(" xmlns%s=\"%s\"" % (
                                k,
                                etree._escape_attrib(v)
                                ))
                    for k, v in list(items):  # no !!!! lexical order
                        if isinstance(k, etree.QName):
                            k = k.text
                        if isinstance(v, etree.QName):
                            v = qnames[v.text]
                        else:
                            v = etree._escape_attrib(v)
                        write(" %s=\"%s\"" % (qnames[k], v))
                if text or len(elem):
                    write(">")
                    if text:
                        write(etree._escape_cdata(text))
                    for e in elem:
                        etree._serialize_xml(write, e, qnames, None)
                    write("</" + tag + ">")
                else:
                    write(" />")
        if elem.tail:
            write(etree._escape_cdata(elem.tail))
    #Redirecting
    etree._serialize_xml = _serialize_xml

if(ver[0]=="2.4"):
#For Python 2.4 there is no serializer. Changing to my method.
    def _escape_attrib(text, encoding=None, replace=etree.string.replace):
        # escape attribute value
        try:
            if encoding:
                try:
                    text = etree._encode(text, encoding)
                except UnicodeError:
                    return etree._encode_entity(text)
            text = replace(text, "&", "&amp;")
            text = replace(text, "\"", "&quot;")
            text = replace(text, "<", "&lt;")
            text = replace(text, ">", "&gt;")
            return text
        except (TypeError, AttributeError):
            etree._raise_serialization_error(text)
    etree._escape_attrib = _escape_attrib
    def _write(self, file, node, encoding, namespaces):
        # write XML to file
        tag = node.tag
        if tag is etree.Comment:
            file.write("<!-- %s -->" % etree._escape_cdata(node.text, encoding))
        elif tag is etree.ProcessingInstruction:
            file.write("<?%s?>" % etree._escape_cdata(node.text, encoding))
        else:
            items = node.items()
            xmlns_items = [] # new namespaces in this scope
            try:
                if isinstance(tag, etree.QName) or tag[:1] == "{":
                    tag, xmlns = fixtag(tag, namespaces)
                    if xmlns: xmlns_items.append(xmlns)
            except TypeError:
                etree._raise_serialization_error(tag)
            file.write("<" + etree._encode(tag, encoding))
            if items or xmlns_items:
                # NO !!!!lexical order
                for k, v in items:
                    try:
                        if isinstance(k, etree.QName) or k[:1] == "{":
                            k, xmlns = fixtag(k, namespaces)
                            if xmlns: xmlns_items.append(xmlns)
                    except TypeError:
                        etree._raise_serialization_error(k)
                    try:
                        if isinstance(v, etree.QName):
                            v, xmlns = fixtag(v, namespaces)
                            if xmlns: xmlns_items.append(xmlns)
                    except TypeError:
                        etree._raise_serialization_error(v)
                    file.write(" %s=\"%s\"" % (etree._encode(k, encoding),
                                               etree._escape_attrib(v, encoding)))
                for k, v in xmlns_items:
                    file.write(" %s=\"%s\"" % (etree._encode(k, encoding),
                                               etree._escape_attrib(v, encoding)))
            if node.text or len(node):
                file.write(">")
                if node.text:
                    file.write(etree._escape_cdata(node.text, encoding))
                for n in node:
                    self._write(file, n, encoding, namespaces)
                file.write("</" + etree._encode(tag, encoding) + ">")
            else:
                file.write(" />")
            for k, v in xmlns_items:
                del namespaces[v]
        if node.tail:
            file.write(etree._escape_cdata(node.tail, encoding))
#Redirecting...
    etree.ElementTree._write=_write
#Location founder function
def loctree(current,root):
    if current == root:
        return("/"+root.tag)
    else:
        c_node=current
        location=""
        if current.get('name'):
            location=current.tag+" "+current.get('name')
        elif len(list(current.keys()))!=0 and current.get(list(current.keys())[0]):
            location=current.tag+" "+list(current.keys())[0]+"="+current.get(list(current.keys())[0])
        else:
            location=current.tag
        build=0
        c_element=root
        while(c_node!=root):
            nlist=list(root)
            nlist.insert(0,root)
            for node in nlist:
                if list(node):
                    nlist+=list(node)
                for child in list(node):
                    if child==c_node:
                        c_node=node
                        if node.get('name'):
                            location=node.tag+" "+node.get('name')+"/"+location
                        elif len(list(node.keys()))!=0 and node.get(list(node.keys())[0]):
                            location=node.tag+" "+list(node.keys())[0]+"="+node.get(list(node.keys())[0])+"/"+location
                        else:
                            location=node.tag+"/"+location
                        if node == root:
                            location="/"+location
                        break
        return(location)  
#MAIN SH FUNCTION
def XMLsh():
    tui=0
    print("Python version: "+ver[0])
    if(ver[0]=="3"):
        fname=input('Enter filename to work with. Default is /var/xapi/state.db: ')
    elif(ver[0]=="2"):
        fname=raw_input('Enter filename to work with. Default is /var/xapi/state.db: ')
    else:
        fname=0
        print("Something with Python version ?")
        return 0
    if fname=="":
        fname="/var/xapi/state.db"
    try:
        tree=etree.parse(fname)
        root=tree.getroot()
    except:
        print("Something goes wrong. Check file? Exiting..")
        return 0
    current=root
    parent=None
    while(tui!=-1):
        if(ver[0]=="3"):
            tui=input('#:')
        elif(ver[0]=="2"):
            tui=raw_input('#:')
        if tui != '':
            tui=list(tui.split())
# Here goes commands
# Command list / ls
            if tui[0]=="list" or tui[0]=="ls":
                for node in list(current):
                    if node.get('name'):
                        print(node.tag+" "+node.get('name'))
                    elif len(list(node.keys()))!=0 and node.get(list(node.keys())[0]):
                        print(node.tag+" "+list(node.keys())[0]+"="+node.get(list(node.keys())[0]))
                    else:
                        print(node.tag)      
                for key in list(current.keys()):
                    print(key+"="+current.get(key))
                if current.text != None:
                    print("Tag text:")
                    print(current.text)
                    
# Command la (list attributes)
            elif tui[0] == "la":
                for key in list(current.keys()):
                    print(key+"="+current.get(key))
                if current.text != None:
                    print("Tag text:")
                    print(current.text)
# Command exit
            elif tui[0] == "exit":
                tui=-1
# Command who
            elif tui[0] == "who":
                print(loctree(current,root))                   
# Command cd
            elif tui[0] == "cd" and len(tui) > 1:    
                if tui[1] != ".." and tui[1] != "/":
                    tui.pop(0)
                    tui=" ".join(tui).strip()
                    tui=tui.split("/")
                    iferror=current
                    for move in tui:
                        if move=='' and len(tui)>2 and tui[1]!=root.tag:
                            current=root
                        if move==root.tag:
                            current=root
                            parent=None
                        for node in list(current):
                            if node.get('name') and node.get('name')==move:
                                parent=current
                                current=node
                            elif node.get('name') and move==node.tag+" "+node.get('name'):
                                parent=current
                                current=node
                            elif len(list(node.keys()))!=0 and move==node.tag+" "+list(node.keys())[0]+"="+node.get(list(node.keys())[0]):
                                parent=current
                                current=node
                            elif str(node.tag)==move:
                                parent=current
                                current=node
                    if iferror==current:
                        print("No such instance.")
                elif tui[1] == "/":
                    current=root
                    parent=None
                elif tui[1] == "..":
                    if parent != None:
                        current=parent
                        c_element=root
                        nlist=list(root)
                        nlist.insert(0,root)
                        for node in nlist:
                            if list(node):
                                nlist+=list(node)
                            for child in list(node):
                                if child==current:
                                    parent=node
                                    break
# Command set
            elif tui[0]=="set":
                tui.pop(0)
                target=tui.pop(0)
                tui=" ".join(tui).strip()
                if target in list(current.keys()):
                    current.set(target,tui)
                else:
                    print("No such attribute")
# Command add
            elif tui[0]=="add":
                tui.pop(0)
                target=tui.pop(0)
                tui=" ".join(tui).strip()
                if target in list(current.keys()):
                    print("Can't add attribute. Already exist.")
                else:
                    current.set(target,tui)
# Command settext
            elif tui[0]=="settext":
                tui.pop(0)
                tui=" ".join(tui).strip()
                current.text=tui
# Command locate, find
            elif tui[0]=="locate" or tui[0]=="find":
                result=""
                mode=tui.pop(0)
                tui=" ".join(tui).strip()
                c_element=root
                nlist=list(root)
                nlist.insert(len(nlist)-1,root)
                for node in nlist:
                    if list(node):
                        nlist+=list(node)
                    for child in list(node):
                        if tui==child.tag or (str(child.tag).find(tui)!=-1 and mode=="find"):
                            print(loctree(child,root))
                        for key in list(child.keys()):
                            if str(key)==tui:
                                print(loctree(child,root)+"/"+tui+"="+str(child.get(tui)))
                            if str(child.get(key))==tui:
                                print(loctree(child,root)+"/"+key+"="+child.get(key))
                            if str(child.text)==tui:
                                print(loctree(child,root)+"/"+tui)
                        if mode=="find":
                            if str(child.text).find(tui)!=-1:
                                print(loctree(child,root)+"/"+child.text)
                            for key in list(child.keys()):
                                if str(key).find(tui)!=-1:
                                    print(loctree(child,root)+"/"+tui+"="+str(child.get(tui)))
                                if str(child.get(key)).find(tui)!=-1:
                                    print(loctree(child,root)+"/"+key+"="+child.get(key))           
# Command xapi
            elif tui[0]=="xapi":
                tui.pop(0)
                tui=" ".join(tui).strip()
                if(tui=="start"):
                    print(call("/etc/init.d/xapi start", shell=True))
                elif(tui=="stop"):
                    print(call("/etc/init.d/xapi stop", shell=True))
                elif(tui=="restart"):
                    print(call("/etc/init.d/xapi restart", shell=True))
                else:
                    print("Usage: xapi <start,stop,restart>")									
# Command save
            elif tui[0]=="save":
                if(ver[0]=="3"):
                    loc=input("Enter filename to save. Default is /var/xapi/state.db: ")
                elif(ver[0]=="2"):
                    loc=raw_input("Enter filename to save. Default is /var/xapi/state.db: ")
                if loc=="":
                        tree.write("/var/xapi/state.db")
                else:
                        tree.write(loc)
# Command ?/help
            elif tui[0]=="?" or tui[0]=="help":
                print("XML shell parser commands:")
                print("ls/list : List childs in current tag")
                print("la : List attributes in current tag")
                print("who : Show current location")
                print("cd : Change directory to <child_name> or <..> to parent node. For enumerated row select: cd row <row_number>") 
                print("set : Change attribute value. Usage: set <attribute> <value>")
                print("add : Add attribute. Usage: add <attribute> <value>")
                print("settext : Change tag text block. Usage: settext <text>")
                print("locate : Locate exact key/value. Usage: locate <value>")
                print("find : Find all ocurrences of value. Usage: find <value>")
                print("xapi : Manage XAPI. Usage: xapi <start/stop/restart>")
                print("save : Save file.")
                print("?/help : Show this message")
                print("! : Debug mode. Direct python command execution. Usage: ! <command>")  
# Debug mode for direct python commands input
            elif tui[0]=="!":
                try:
                    print(eval(tui[1]))
                except:
                    print ("Something goes wrong..")
# Incorrect command
            else:
                tui=" ".join(tui).strip()
                print("No such command "+tui)
XMLsh()
