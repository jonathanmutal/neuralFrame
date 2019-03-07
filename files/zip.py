import zipfile
import os
import shutil


from files.xliff import Xliff


class Zip:
    """
    This class abstract all the method for zip and unzip.
    """
    def __init__(self, path, configuration):
        """
        extract a zip file from path
        :path: a string path for the zip
        """
        zip_ref = zipfile.ZipFile(path, 'r')
        zip_ref.extractall()
        zip_ref.close()

        # path[:-len('.zip')]
        self.__outpath = os.path.join(path, '{0}_out.zip'.format(path[:-4]))
        self.__files =  zip_ref.filelist
        self.__config = configuration

        self.__input_files = []
        self.__output_files = []
        for f in zip_ref.filelist:
            dir_name = os.path.abspath(os.path.dirname(f.filename))
            file_name = os.path.basename(f.filename)
            abs_path = os.path.join(dir_name, file_name)
            if not file_name:
                continue
            self.__input_files.append(abs_path)
            self.__output_files.append('{0}_out.docx.xlf'.format(abs_path[:-9]))

    def generate_traduction(self):
        """
        generate the traduction for each folder.
        """
        for f_in, f_out in zip(self.__input_files, self.__output_files): 
            lang = 'fr' if 'fr' in f_in.lower() else 'it'
            Xliff(f_in, self.__config, lang).put_translated_sentences(f_out)


    def generate_zip(self):
        """
        generate the final zip.
        """
        zip_name = zipfile.ZipFile(self.__outpath, 'w')
        for f_in, f_out in zip(self.__input_files, self.__output_files):
            zip_name.write(f_out, os.path.join(os.path.basename(os.path.dirname(f_out)), os.path.basename(f_out)))
            shutil.rmtree(os.path.abspath(os.path.dirname(f_in)))
        zip_name.close()
