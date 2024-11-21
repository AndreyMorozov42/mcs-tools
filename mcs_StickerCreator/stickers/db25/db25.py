import datetime
import json
import os
from copy import copy, deepcopy

from reportlab.lib.units import mm
from mcs_StickerCreator.constants import RADIUS_REF_POINT
from mcs_StickerCreator.stickers.db25.create_pdf_dxf import create_pdf_dxf
from mcs_StickerCreator.stickers.db25.sticker import Sticker

PATH_TO_METADATA = "metadata.json"


def db25var1_create_pdf_dxf(input_file, sign):
    with open(PATH_TO_METADATA, "r") as file:
        metadata = json.load(file)

    # создание шаблона
    template_stickers = []
    for stc in metadata["stickers"]:
        s = Sticker()
        for attr in stc.keys():
            if attr == "sn" and sign == "sn":
                setattr(s, "path_to_svg", stc[attr])
            if attr == "lot" and sign == "lot":
                setattr(s, "path_to_svg", stc[attr])
            if attr == "mm_width" or attr == "mm_height":
                setattr(s, attr, stc[attr] * mm)
            if attr == "dxf":
                setattr(s, "path_to_dxf", stc[attr])
            if attr == "inverted":
                setattr(s, attr, stc[attr])
            if attr == "labels":
                setattr(s, attr, stc[attr])
        template_stickers.append(deepcopy(s))

    # чтение данных и генерация стикеров
    with open(input_file, "r") as file:
        stickers = []
        ind_s = 0
        for data in file.readlines():

            if data == "\n":
                continue

            data = data.replace("\n", "").split(";")
            s = deepcopy(template_stickers[ind_s])
            s.initialize()
            s.set_label(data)
            stickers.append(s)

            if ind_s == len(template_stickers) - 1:
                ind_s = 0
            else:
                ind_s += 1

    # create dir with time processing for saving the result
    to_save = f"./output/{datetime.datetime.now().isoformat()[:-7].replace(':', '-')}"
    if not os.path.exists(to_save):
        os.makedirs(to_save)

    if len(stickers) > 0:
        create_pdf_dxf(
            stickers=stickers,
            dx=-7 * mm, dy=1 * mm,
            x_pad=2 * RADIUS_REF_POINT + mm, y_pad=RADIUS_REF_POINT,
            dir_to_save=to_save,
        )




if __name__ == "__main__":
    db25var1_create_pdf_dxf(
        r"C:\Users\andmo\OneDrive\Desktop\my-dev-work\mcs-Tools\mcs_StickerCreator\input\task_15-11-2024\input5.txt",
        sign="sn"
    )

