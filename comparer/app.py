from pathlib import Path
from typing import List, Tuple
import pandas as pd
from comparer import get_logger

from comparer.templates import FileRepository


class Application:
    def __init__(self, file_repo: FileRepository, debug: bool = False) -> None:
        self.file_repo = file_repo
        self.debug = debug
        self.logger = get_logger()

    def basic_statistics(self, chosen_files: List[Path]) -> None:
        df_list = self._assign_table(chosen_files)
        return self._summarize_basic(df_list, self.debug)

    def full_statistics(self,chosen_files: List[Path]) -> None:
        return None

    def visualize(self,chosen_files: List[Path]) -> None:
        return None

    def _summarize_basic(self,df_list: List[Tuple[pd.DataFrame, int]], debug: bool = False) -> None:
        for tuple in df_list:
            df = tuple[0]
            #Bottom Table
            if tuple[1] == 0:
                number_fill = 0
                for column, column1 in zip(df['major_equipment'].notna(), df['major_equipment_parsed'].isna()):
                    if column and column1:
                        number_fill += 1
                number_dex = 0
                for column in df['drawing_description']:
                    if column == 'Exception':
                        number_dex += 1
                number_nex = 0
                for column in df['drawing_number']:
                    if column == 'Exception':
                        number_nex += 1
                number_tit = 0
                for column in df['drawing_title_name']:
                    if column == 'Exception':
                        number_tit += 1
                if debug:
                    self.logger.debug(" ")
                    self.logger.debug('-------------Bottom Table Statistics-------------')
                    self.logger.debug(f'Found {number_fill} cells where Major Equipment is filled and Major Equipment Parse isn\'t')
                    self.logger.debug((f'Found {number_dex} exceptions in Drawing Description'))
                    self.logger.debug((f'Found {number_nex} exceptions in Drawing Number'))
                    self.logger.debug((f'Found {number_tit} exceptions in Drawing Title Name'))
                    self.logger.debug(" ")
        return None

    def _assign_table(self, chosen_files: List[Path]) -> List[Tuple[pd.DataFrame, int]]:
       
        df_list: List[Tuple[pd.DataFrame, int]] = []
        for file in chosen_files:
            if "bottom_tables" in str(file):
                print("dupa", str(file))
                fields = ["filename", "drawing_number", "drawing_title_name", "drawing_description", "major_equipment", "major_equipment_parsed"]
                df = pd.read_csv(str(file), sep = ",", usecols= fields)
                df_list.append((df,0))
            elif 'equipment' in str(file):
                fields = ["SERVICE DESCRIPTION", "YARD NO", "Equipment Code", "eq_origin", "debug_equipment_method", "Scraped Equipment Type"]
                df = pd.read_csv(str(file), sep = ",", usecols = fields)
                df_list.append((df,1))
            elif "tag_assignments" in str(file):
                fields = ['Equipment Code', 'Scraped Equipment Type', 'Drawing Number', 'Sensor Name']
                df = pd.read_csv(str(file), sep = ",", usecols = fields)
                df_list.append((df,2))
            else:
                raise ValueError("Csv file with invalid name!")
        return df_list