import yaml
import tempfile


from opennmt.runner import Runner
from opennmt.models.model import Model
from opennmt.config import load_config, load_model


class Neural:
    """
    This class will be wrapped class from openNMT-tf.
    """
    def __init__(self, config):
        """
        Configuration for the model
        :config: the configuration for the model.
          -- :config_path: a list of path to configure the model
          -- :model_type: a model type
          -- :check_point_path: a check_point for the path
        """
        self.__config = {}
        for config_path in config['config_path']:
            with open(config_path, 'r') as f:
                self.__config.update(yaml.load(f.read()))
        self.__config['model_type'] = config['model_type']
        self.__config['checkpoint_path'] = config['checkpoint_path']
        
        
        model = load_model(self.__config["model_dir"], model_name=self.__config['model_type'])
        self.model = Runner(model, self.__config)


    def infer(self, sentences):
        """
        This method is to infer.
        :sentences: a list of preprocessed sentences.
        return a sentence translated.
        """
        # we are using opennmt-tf so we should open a file to write sentences to translated.
        file_to_translate = tempfile.NamedTemporaryFile('w', delete=False)
        file_to_translate.writelines(sentences)
        file_to_translate.close()

        file_translated = tempfile.NamedTemporaryFile('w', delete=False)
        file_translated.close()
        self.model.infer(features_file=file_to_translate.name, predictions_file=file_translated.name, checkpoint_path=self.__config['checkpoint_path'])
        with open(file_translated.name, 'r') as f:
            sentences_translated = f.readlines()
        return sentences_translated
