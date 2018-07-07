from pathlib import Path
import os
import subprocess

if __name__ in '__main__':
    print('年度')
    year = input('>> ')

    print('公報種類を入力してください(A,A5,S,S5,T,T5)')
    in_filetype = input('>> ')

    tif_dir_path = "/mnt/Drobo/TIF_files/" + in_filetype + '/' + str(year)

    path_list = []
    tif_path = Path(tif_dir_path)
    path_list += list(tif_path.glob("**/*.tif"))

    for pl in path_list:
        tif_file_path = str(pl)
        png_file_path = tif_file_path.replace('TIF_files','PNG_files').replace('.tif','')
        os.makedirs(png_file_path, exist_ok=True)

        tmp = png_file_path.split('/')[-1]
        png_file_path += '/' + tmp + '.png'

        subprocess.call(('convert ' + tif_file_path + ' ' + png_file_path), shell=True)
