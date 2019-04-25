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
        self.__flat_list = lambda l: [item for item in l for item in sublist]
        self.__clean_source = lambda list_: list((re.sub('<.+?>', '', elem), reg) for elem, reg in list_)
        self.__translator = translator(configuration, lang)

        with open(xliff_path, 'r', encoding='utf-8') as xml:
            self.__xliff = xml.read()

    def __to_translate(self,sent):
        if re.findall('^(.+)?</source><target state-qualifier="leveraged-tm"/>', sent):
            sent, label = re.split('</source><target state-qualifier="leveraged-tm"/>', sent), '</source><target (state-qualifier="leveraged-tm")/>'
        elif re.findall('^(.+)?</source><target state-qualifier="fuzzy-match"/>', sent):
            sent, label =  re.split('</source><target state-qualifier="fuzzy-match"/>', sent), '</source><target (state-qualifier="fuzzy-match")/>'
        elif re.findall('^(.+)?</source><target state-qualifier="x-fuzzy-forward"/>', sent):
            sent, label = re.split('</source><target state-qualifier="x-fuzzy-forward"/>', sent), '</source><target (state-qualifier="x-fuzzy-forward")/>'
        elif re.findall('^(.+)?</source><target state-qualifier="x-alphanum"/>', sent):
            sent, label = re.split('</source><target state-qualifier="x-alphanum"/>', sent), '</source><target (state-qualifier="x-alphanum")/>'
        elif re.findall('^(.+)?</source><target state-qualifier="leveraged-inherited/>', sent):
            sent, label = re.split('</source><target state-qualifier="leveraged-inherited/>', sent), '</source><target (state-qualifier="leveraged-inherited)/>'
        elif re.findall('^(.+)?</source><target/>', sent):
            sent, label = re.split('</source><target/>', sent), '</source><target/>'
        else:
            return '', ''
        return sent[0].split('<source>')[-1], label

    def __get_source_sentences(self):
        """
        return the clean source needed to translate
        """
        # delete all the header
        new_xml = self.__delete_header.sub('', self.__xliff)
        # take the trans_units
        trans_units = self.__split_translation(new_xml)
        ## get all the source-target that are needeed to translate.
        to_translate = []
        for transunit in trans_units:
            for sent in transunit.split('<source>'):
                to_translate.append(self.__to_translate(sent))
        print(to_translate)
        ## extract the source and flat the list and It's ready to translate.
        source_target = list(filter(lambda sent: len(sent[0]) > 0, to_translate))
        return self.__clean_source(source_target)

    def put_translated_sentences(self, output_file):
        """
        :output_file: the outputfile should be abs directory+file.
        """
        sentences_to_translate = self.__get_source_sentences()
        sentences_t = self.__translator.translate_sentences([sent for sent, reg in sentences_to_translate])

        string_xml = self.__xliff
        for index, sent in enumerate(sentences_t):
            if '</source><target/>' == sentences_to_translate[index][1]:
                string_xml = re.sub(sentences_to_translate[index][1],
                                    r'</source><target state="translated">{0}</target>'.format(sent),
                                    string_xml, 1)
            else:
                string_xml = re.sub(sentences_to_translate[index][1],
                    r'</source><target \1 state="translated">{0}</target>'.format(sent),
                    string_xml, 1)

        with open(output_file, 'w') as xml_output:
            xml_output.write(string_xml)

        print('The output file is ready.')
