import os
import struct
import base64


class File_Type:

    @staticmethod
    def typeList():
        type_dict = {'jpg': ['FFD8FFE000104A464946', 'FFD8FFE1001845786966', 'FFD8FFE100D645786966'],
                     'png': ['89504E470D0A1A0A0000'],
                     'gif': ['47494638396126026F01', '4749463839613306C508'],
                     'tif': ['49492A', '4D4D'],
                     'bmp': ['424D8E1B030000000000'],

                     'html': ['3C21444F435459504520'],
                     'htm': ['3C21646F637479706520'],
                     'css': ['48544D4C207B0D0A0942'],
                     'js': ['696B2E71623D696B2E71'],
                     'rtf': ['7B5C727466315C616E73'],

                     'eml': ['46726F6D3A203D3F6762'],
                     'mdb': ['5374616E64617264204A'],
                     'ps': ['252150532D41646F6265'],

                     'pdf': ['255044462D312E', '255044462D312E340A25', '255044462D312E350D0A'],
                     'rmvb': ['2E524D46000000120001'],
                     'flv': ['464C5601050000000900'],
                     'mp4': ['00000020667479706D70'],
                     'mpg': ['000001BA210001000180'],

                     'wmv': ['3026B2758E66CF11A6D9'],
                     'wav': ['52494646E27807005741'],
                     'avi': ['52494646D07D60074156'],
                     'mid': ['4D546864000000060001'],

                     'zip': ['504B0304140000000800', '504B0304140000080800', '504B03040A0000080000',
                             '504B0304140008080800'],
                     'rar': ['526172211A0700CF9073'],
                     'ini': ['235468697320636F6E66'],
                     'jar': ['504B03040A0000080000'],
                     'exe': ['4D5A9000030000000400'],
                     'jsp': ['3C25402070616765206C'],
                     'mf': ['4D616E69666573742D56'],

                     'xml': ['3C3F786D6C2076657273'],
                     'sql': ['494E5345525420494E54'],
                     'java': ['7061636B616765207765'],
                     'bat': ['406563686F206F66660D'],
                     'gz': ['1F8B0800000000000000'],

                     'properties': ['6C6F67346A2E726F6F74'],
                     'class': ['CAFEBABE0000002E0041'],
                     'docx': ['504B0304140006000800', '504B03040A0000000000'],
                     'doc': ['D0CF11E0A1B11AE10000', 'D0CF11E0A1B11AE10609'],
                     # 'xls': ['D0CF11E0A1B11AE10000'],
                     # 'xlsx': ['504B03040A0000000000'],
                     'torrent': ['6431303A637265617465'],

                     'mov': ['6D6F6F76'],
                     'wpd': ['FF575043'],
                     'dbx': ['CFAD12FEC5FD746F'],
                     'pst': ['2142444E'],
                     'qdf': ['AC9EBD8F'],
                     'pwl': ['E3828596'],
                     'ram': ['2E7261FD'],
                     'ZBS': ['504B03040A0000000800'],
                     }
        ret = {}
        for k_hex, v_prefix in type_dict.items():
            ret[k_hex] = v_prefix
        return ret

    @staticmethod
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

    @staticmethod
    def bytes2hex_up(bytes):
        num = len(bytes)
        hexstr = u""
        for i in range(num):
            t = u"%x" % bytes[i]
            if len(t) % 2:
                hexstr += u""
            hexstr += t
        return hexstr.upper()

    @staticmethod
    def stream_type(stream, header={}):
        tl = File_Type.typeList()
        ftype = None
        for type_name, hcode_list in tl.items():
            flag = False
            for hcode in hcode_list:
                s_hcode = File_Type.bytes2hex(stream)
                # print("转成十六进制的编码", s_hcode, '=', "头文件", hcode, type_name)
                if s_hcode == hcode:
                    flag = True
                    break
                elif s_hcode != hcode:
                    numOfBytes = int(len(hcode) / 2)
                    hbytes = struct.unpack_from("B" * numOfBytes, stream[0:numOfBytes])
                    s_hcode = File_Type.bytes2hex_up(hbytes)
                    # print("转成十六进制的编码", s_hcode, '=', "头文件", hcode, type_name)
                    if s_hcode == hcode:
                        flag = True
                        break
            if flag:
                ftype = type_name
                break
        ftype_list = ['doc', 'xls', 'docx', 'xlsx', None]
        if ftype in ftype_list:
            new_ftype = File_Type.get_file_stream(header)
            if new_ftype:
                ftype = new_ftype
        return ftype

    @staticmethod
    def get_file_stream(header):
        finename = header.get('Content-Disposition')
        content_type = header.get('Content-Type')
        if finename:
            file_stream = os.path.splitext(finename)[-1].replace('"', '').replace("", "").replace(".", "").replace(";",
                                                                                                                   "")
            return file_stream
        elif content_type:
            content_type_map = {
                'audio/aac': 'aac',
                'application/x-abiword': 'abw',
                'application/x-freearc': 'arc',
                'video/x-msvideo': 'avi',
                'application/vnd.amazon.ebook': 'azw',
                'application/octet-stream': 'bin',
                'image/bmp': 'bmp',
                'application/x-bzip': 'bz',
                'application/x-bzip2': 'bz2',
                'application/x-csh': 'csh',
                'text/css': 'css',
                'text/csv': 'csv',
                'application/msword': 'doc',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
                'application/vnd.ms-fontobject': 'eot',
                'application/epub+zip': 'epub',
                'image/gif': 'gif',
                'text/html': 'htm',
                'image/vnd.microsoft.icon': 'ico',
                'text/calendar': 'ics',
                'application/java-archive': 'jar',
                'image/jpeg': 'jpg',
                'text/javascript': 'js',
                'application/json': 'json',
                'application/ld+json': 'jsonld',
                'audio/midi': 'mid',
                'audio/mpeg': 'mp3',
                'video/mpeg': 'mpeg',
                'application/vnd.apple.installer+xml': 'mpkg',
                'application/vnd.oasis.opendocument.presentation': 'odp',
                'application/vnd.oasis.opendocument.spreadsheet': 'ods',
                'application/vnd.oasis.opendocument.text': 'odt',
                'audio/ogg': 'oga',
                'video/ogg': 'ogv',
                'application/ogg': 'ogx',
                'font/otf': 'otf',
                'image/png': 'png',
                'application/pdf': 'pdf',
                'application/vnd.ms-powerpoint': 'ppt',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
                'application/x-rar-compressed': 'rar',
                'application/rtf': 'rtf',
                'application/x-sh': 'sh',
                'image/svg+xml': 'svg',
                'application/x-shockwave-flash': 'swf',
                'application/x-tar': 'tar',
                'image/tiff': 'tif',
                'font/ttf': 'ttf',
                'text/plain': 'txt',
                'application/vnd.visio': 'vsd',
                'audio/wav': 'wav',
                'audio/webm': 'weba',
                'video/webm': 'webm',
                'image/webp': 'webp',
                'font/woff': 'woff',
                'font/woff2': 'woff2',
                'application/xhtml+xml': 'xhtml',
                'application/vnd.ms-excel': 'xls',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
                'application/xml': 'xml',
                'application/vnd.mozilla.xul+xml': 'xul',
                'application/zip': 'zip',
                'video/3gpp': '3gp',
                'video/3gpp2': '3g2',
                'application/x-7z-compressed': '7z'}
            ftype = content_type_map.get(content_type)
            return ftype
