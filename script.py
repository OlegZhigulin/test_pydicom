import csv
import os
from glob import glob
from tempfile import TemporaryDirectory

import pydicom
from tqdm import tqdm

path_to_files = 'c:/Dev/machine_learning/recruit/src/*'
output_file_path = 'c:/Dev/machine_learning/recruit/cache'

TAG = 'PatientName'
NEW_NAME = 'SOPInstanceUID'
SUFFIX = '.dcm'
temp = TemporaryDirectory()

# Какая была задумка изначально, но изза документации я не разобрался
# Мы берем файл, сохраняем путь
# копируем его во временное хранилище или
# переменную (чтобы не редактировать исходники)
# делаем анонимным
# после из временного хранилища в другую папку расладываем файлы как нужно
# записываем пути


def anonymaze(dicom_file, tag=None):
    if tag is not None:
        try:
            if dicom_file.get(TAG):
                del dicom_file[TAG]
        except KeyError as error:
            print(error)


def main():
    set_dirs = set()
    with open('dependence.csv', 'w', encoding='utf-8', newline='') as file:
        columns = ['old_path', 'new_path']
        writer = csv.DictWriter(file,
                                fieldnames=columns,
                                delimiter=';',
                                quoting=csv.QUOTE_NONNUMERIC
                                )
        writer.writeheader()
        for path_to_file in tqdm(glob(path_to_files)):
            try:
                dicom_file = pydicom.dcmread(path_to_file)
                anonymaze(dicom_file, tag=TAG)
                new_name = dicom_file.get(NEW_NAME) + SUFFIX
                study = dicom_file.get(
                    'StudyInstanceUID', 'unidentified_study')
                series = dicom_file.get(
                    'SeriesInstanceUID', 'unidentified_series')
                new_path = f'{output_file_path}/{study}/{series}/'
                writer.writerow(
                    {
                        'old_path': f'{path_to_file}',
                        'new_path': f'{new_path}{new_name}'
                    }
                )
                if new_path not in set_dirs:
                    set_dirs.add(new_path)
                    try:
                        os.makedirs(new_path)
                    except FileExistsError:
                        print('папка уже существует')
                dicom_file.save_as(
                    filename=f'{new_path}{new_name}',
                    write_like_original=False
                )
            except FileExistsError:
                print('файл отсутствует')


if __name__ == '__main__':
    main()
