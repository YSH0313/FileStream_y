# -*- coding: utf-8 -*-
# @Author: yuanshaohang
# @Date: 2023-03-15- 14:32:07
# @Version: 1.0.0
# @Description: TODO

import os
import struct
import base64
from .filetype_map import type_dict, content_type_map


def typeList():
    ret = {}
    for k_hex, v_prefix in type_dict.items():
        ret[k_hex] = v_prefix
    return ret


def bytes2hex(bytes):
    # num = len(bytes)
    hexstr = u""
    for i in range(10):
        try:
            t = u"%x" % bytes[i]
            if len(t) % 2:
                hexstr += u"0"
            hexstr += t
        except IndexError:
            return ''
    return hexstr.upper()


def bytes2hex_up(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u""
        hexstr += t
    return hexstr.upper()


def stream_type(stream, header={}):
    tl = typeList()
    ftype = None
    for type_name, hcode_list in tl.items():
        flag = False
        for hcode in hcode_list:
            s_hcode = bytes2hex(stream)
            # print("转成十六进制的编码", s_hcode, '=', "头文件", hcode, type_name)
            if s_hcode == hcode:
                flag = True
                break
            elif s_hcode != hcode:
                numOfBytes = int(len(hcode) / 2)
                hbytes = struct.unpack_from("B" * numOfBytes, stream[0:numOfBytes])
                s_hcode = bytes2hex_up(hbytes)
                # print("转成十六进制的编码", s_hcode, '=', "头文件", hcode, type_name)
                if s_hcode == hcode:
                    flag = True
                    break
        if flag:
            ftype = type_name
            break
    ftype_list = ['doc', 'xls', 'docx', 'xlsx', None]
    if ftype in ftype_list:
        new_ftype = get_file_stream(header)
        if new_ftype:
            ftype = new_ftype
    return ftype


def get_file_stream(header):
    finename = header.get('Content-Disposition')
    content_type = header.get('Content-Type')
    if finename:
        file_stream = os.path.splitext(finename)[-1].replace('"', '').replace("", "").replace(".", "").replace(";",
                                                                                                               "")
        return file_stream
    elif content_type:
        ftype = content_type_map.get(content_type)
        return ftype
