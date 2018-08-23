from modules.e_object import e_object
import os.path
import os
import yaml
import json

class File(e_object):
        def __init__(self):
            super().__init__()
            self.f_object={}
            self.f_object_list=[]

        @staticmethod
        def read_file(file_name):
            file_data=""
            with open(file_name,"r") as fo:
                for file_line in fo:

                    file_data+=file_line.rstrip("\n")


            return file_data
        
        def json(self,file_name):
            file_data=str(self.read_file_only(file_name))
            return jsonData(**(json.loads(file_data)))


        @staticmethod
        def read_file_only(file_name):
            file_data=""
            with open(file_name,"r",encoding="utf-8") as fo:

                    file_data=fo.read()

            return file_data

        @staticmethod
        def file2Dic(file_name,line_separator):
            line_delim=None
            current_delim=[]
            doc_delim=[]
            is_delim_found=False

            with open(file_name,"r") as fo:
                for line in fo:
                    strip_line=line.strip('\n')

                    if(strip_line==line_separator):
                        current_delim.append(line)
                        doc_delim.append(current_delim)
                        current_delim=[]

                    else:

                        current_delim.append(line)

                doc_delim.append(current_delim)

            return doc_delim

        def viewFObjectData(self):
            print(self.f_object_list)		

        """find data in the list of fobject
        """

        def findFObjectData(self,search_key,prop_separator="="):

            for prop in self.f_object_list:

                for prop_data in prop:
                    prop_data_list=prop_data.split(prop_separator)
                    key=(prop_data_list[0]).strip()

                    value=(prop_data_list[1]).strip()

                    if("".join(search_key.split())==value):
                        return True

            return False
        """

           [Parameter3]: character that separate the key and the value
        """

        def file2ObjProp(self,file_name,line_separator,prop_separator="="):
            line_delim=None
            current_delim=[]
            doc_delim=[]
            is_delim_found=False
            FObject=self.define_class("FObject")
            parent_separator=""
            
            with open(file_name,"r") as fo:
                
                for line in fo:
                    strip_line=line.strip('\n')
                    
                    if(not line.startswith("\t")):
                        parent_separator=strip_line
   
                    if(strip_line in line_separator):
                        
                        if(len(current_delim) > 0):
                            doc_delim.append(current_delim)
                        current_delim=[]

                    else:
                        if(parent_separator in line_separator):
                            print(line)
                            if(line.startswith("\t")):
                                current_delim.append(line)

                doc_delim.append(current_delim)
                print(current_delim)

            self.f_object_list=doc_delim
            
            i=1
            for prop in doc_delim:
                self.f_object[i]=FObject()
                for prop_data in prop:
                    prop_data_list=prop_data.split(prop_separator)
                    key=(prop_data_list[0]).strip()

                    value=prop_data_list[1]
                    self.define_class_prop(self.f_object[i],key,value)
                i+=1

            return self.f_object


        #@staticmethod
        #def delLineInFile(file_name,line_separator,line_to_delete):
        #	doc_list=File.file2Dic(file_name,line_separator)

        """Use to delete a line
        """
        @staticmethod
        def delLineInFile(file_name,line_separator,line_to_delete):
            doc_list=File.file2Dic(file_name,line_separator)

            current_index=0

            del_index=[]


            for list_data in doc_list:

                for list_data_item in list_data:
                    strip_list_data_item=list_data_item.strip()
                    if(strip_list_data_item in line_to_delete):

                        del_index.append(current_index)

                        break
                current_index+=1

            i=0
            if(len(del_index) > 0):	
                #delete all the index that matches the search
                for index in del_index:
                    #decrement the value of i from the index key
                    index-=i

                    del doc_list[index]

                    i+=1
            #print(doc_list)
            #return doc_list
            File.dict2File(file_name,doc_list)


        @staticmethod
        def modFile(file_name,dict_data,separator=":"):
            docs={}
            list_doc=[]
            file_data=[]

            try:
                with open(file_name,"r") as stream_file:
                    for line in stream_file:
                        strip_line=line.strip()
                        if not strip_line.startswith("#"):
                            str2list=line.split(separator)
                            if(len(str2list) > 1):

                                key=str2list[0]

                                value=str2list[1]
                                if key in dict_data:
                                    value=dict_data[key]

                                line_data="%s:%s\n"%(key,value)


                                file_data.append(line_data)
                        else:
                            file_data.append(line)


            except FileNotFoundError as ex:
                print(ex)

            #print(file_data)

            File.list2File(file_name,file_data)				


        @staticmethod
        def list2File(file_name,list_data):
            with open(file_name,"w") as fi:

                data_len=len(list_data)

                for data in list_data:

                    fi.write(data)

        @staticmethod
        def dict2File(file_name,list_data):
            with open(file_name,"w") as fi:
                data_len=len(list_data)
                i=0
                for data in list_data:

                    for data_item in data:

                        #print(data_item)
                        fi.write(data_item)



        def del_file(self,file_name):
            self.run_shell("rm -rf "+file_name)

        def is_file_exist(self,path_to_file_name):
            #is_file_exists=False
            is_file_exists=os.path.isfile(path_to_file_name)
            return is_file_exists

        @staticmethod
        def read_yaml_file(file_name,separator=":"):
            docs={}
            list_doc=[]

            try:
                with open(file_name,"r") as stream_file:
                    for line in stream_file:
                        strip_line=line.strip()
                        if not strip_line.startswith("#"):
                            str2list=line.split(separator)
                            if(len(str2list) > 1):

                                key=str2list[0]

                                value=str2list[1]

                                docs[key]=value

            except FileNotFoundError as ex:
                print(ex)

            return docs

        @staticmethod
        def write_append_to(file_name,data_to_append):

            with open(file_name,"a+") as fi_stream:

                fi_stream.write(data_to_append+"\n")


        @staticmethod
        def write_to(file_name,data_to_write):

            with open(file_name,"w") as fi_stream:
                fi_stream.write(data_to_write)


        @staticmethod
        def mkdir(dir_name):

            try:
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)
            except Exception as ex:
                print(ex)
                
                
class jsonData():
    """This class is use to store the data send by the client 
       as class object data, a small reminder is the data has been send as a json
       format.Every json key represent the object key
    """
    def __init__(self,**entities):
        self.__dict__.update(entities)

