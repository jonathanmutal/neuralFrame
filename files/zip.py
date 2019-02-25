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

        self.__outpath = os.path.join(path, '{0}_out.zip'.format(path[:-4]))
        self.__files =  zip_ref.filelist
        self.__config = configuration

    def generate_traduction(self):
        """
        generate the traduction for each folder.
        """
        for f in self.__files:
            dir_name = os.path.abspath(os.path.dirname(f.filename))
            file_name = os.path.basename(f.filename)
            abs_path = os.path.join(dir_name, file_name)
            lang = 'fr' if 'fr' in dir_name else 'it'
            Xliff(abs_path, self.__config, lang).put_translated_sentences('{0}_out.docx.xlf'.format(abs_path[:-9]))
            os.remove(abs_path)


    def generate_zip(self):
        zip_name = zipfile.ZipFile(self.__outpath, 'w')
        for f in self.__files:
            zip_name.write(f.filename[:-9] + '_out.docx.xlf')
        shutil.rmtree(os.path.abspath(os.path.dirname(f.filename)))
        zip_name.close()
