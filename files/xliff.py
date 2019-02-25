import re


from translate.translate import Translation


class Xliff:
    """
    A class to handle xliff from XTM.
    """
    def __init__(self, xliff_path, configuration, lang='fr', translator=Translation):
        """
        :xliff_path: a path to read the xliff
        :configuration: the model configuration
        :lang: the lang for the model
        :translator: a model to translate
        """
        self.__delete_header = re.compile('<header>.+</header>', re.DOTALL)
        self.__split_translation = lambda xml: re.findall('<trans-unit .+?>.+?</trans-unit>', xml)
        self.__get_source = lambda trans_unit: re.findall('<source.*?>.*?<target.*?/>', trans_unit)
        self.__remove_empty_lists = lambda list_: [elem for elem in list_ if elem]
        self.__flat_list = lambda l: [item for sublist in l for item in sublist]
        self.__clean_source = lambda list_: list(re.sub('<.+?>', '', elem) for elem in list_)
        self.__translator = translator(configuration, lang)

        with open(xliff_path, 'r', encoding='utf-8') as xml:
            self.__xliff = xml.read()


    def __get_source_sentences(self):
        """
        return the clean source needed to translate
        """
        # delete all the header
        new_xml = self.__delete_header.sub('', self.__xliff)
        # take the trans_units
        trans_units = self.__split_translation(new_xml)
        ## get all the source-target that are needeed to translate.
        source_target = list(map(lambda trans_unit: self.__get_source(trans_unit), trans_units))
        ## extract the source and flat the list and It's ready to translate.
        source_target = self.__flat_list(self.__remove_empty_lists(source_target))
        return self.__clean_source(source_target)

    def put_translated_sentences(self, output_file):
        """
        :output_file: the outputfile should be abs directory+file.
        """
        sentences_to_translate = self.__get_source_sentences()
        sentences_t = self.__translator.translate_sentences(sentences_to_translate)
        self.__translator.close()

        string_xml = self.__xliff
        for sent in sentences_t:
            string_xml = re.sub('</source><target(.*?)/>',
                r'</source><target\1 state="translated">{0}</target>'.format(sent),
                string_xml, 1)

        with open(output_file, 'w') as xml_output:
            xml_output.write(string_xml)

        print('The output file is ready.')
