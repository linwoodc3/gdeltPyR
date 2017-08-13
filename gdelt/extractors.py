# #!/usr/bin/python
# # -*- coding: utf-8 -*-
#
# # Author:
# # Linwood Creekmore
# # Email: valinvescap@gmail.com
#
# ##################################
# # Standard library imports
# ##################################
# import re
# import zipfile
# from io import BytesIO
# import warnings, datetime
#
# ##################################
# # Third party imports
# ##################################
# import pandas as pd
# import requests
#
# ##################################
# # Local imports
# ##################################
#
# def _downloadAndExtract(gdeltUrl):
#     """Downloads and extracts GDELT zips without saving to disk"""
#
#     response = requests.get(gdeltUrl, stream=True)
#     zipdata = BytesIO()
#     zipdata.write(response.content)
#     gdelt_zipfile = zipfile.ZipFile(zipdata, 'r')
#     name = re.search('(([\d]{4,}).*)',
#                      gdelt_zipfile.namelist()[0]).group().replace('.zip', "")
#     data = gdelt_zipfile.read(name)
#     gdelt_zipfile.close()
#     del zipdata, gdelt_zipfile, name, response
#     return pd.read_csv(BytesIO(data), delimiter='\t', header=None)
#
#
# def _normalpull(url,table=None):
#     """When single string url, just download it"""
#     r = requests.get(url, timeout=5)
#     # print(len(r.content))
#     r.raise_for_status()
#
#     # print (multiprocessing.Process(name=multiprocessing.current_process().name).is_alive())
#     try:
#         buffer = BytesIO(r.content)
#         # print(buffer.seek())
#
#         if table == 'events':
#             frame = pd.read_csv(buffer, compression='zip', sep='\t',
#                                 header=None, warn_bad_lines=False,
#                                 dtype={26: 'str', 27: 'str', 28: 'str'},
#                                 parse_dates=[1, 2])
#             # print(frame.shape)
#         elif table == 'gkg':
#             frame = pd.read_csv(buffer, compression='zip', sep='\t',
#                                 parse_dates=['DATE'], warn_bad_lines=False)
#
#         else:
#
#             frame = pd.read_csv(buffer, compression='zip', sep='\t',
#                                 header=None, warn_bad_lines=False)
#         end = datetime.datetime.now() - start
#         # print ("{0} with id {1} finished processing in {2}".format(proc_name,proc,end))
#         buffer.flush()
#         buffer.close()
#         # print(frame.shape)
#         return frame
#
#     except:
#         try:
#             message = "GDELT did not return data for date time " \
#                       "{0}".format(re.search('[0-9]{4,18}', url).group())
#             warnings.warn(message)
#         except:
#             message = "No data returned for {0}".format(r.url)
#             warnings.warn(message)