

```python
import requests
import lxml.html as lh

gdelt_base_url = 'http://data.gdeltproject.org/events/'
gdelt_gkg_url = 'http://api.gdeltproject.org/api/v1/gkg_geojson'
# get the list of all the links on the gdelt file page
page = requests.get(gdelt_base_url+'index.html')
doc = lh.fromstring(page.content)
link_list = doc.xpath("//*/ul/li/a/@href")

# separate out those links that begin with four digits 
file_list = [x for x in link_list if str.isdigit(x[0:4])]

```


```python
masterListUrl = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
directory = requests.get(masterListUrl)
results = directory.content.split('\n')
```


```python
results
```




    ['150383 297a16b493de7cf6ca809a7cc31d0b93 http://data.gdeltproject.org/gdeltv2/20150218230000.export.CSV.zip',
     '318084 bb27f78ba45f69a17ea6ed7755e9f8ff http://data.gdeltproject.org/gdeltv2/20150218230000.mentions.CSV.zip',
     '10768507 ea8dde0beb0ba98810a92db068c0ce99 http://data.gdeltproject.org/gdeltv2/20150218230000.gkg.csv.zip',
     '149211 2a91041d7e72b0fc6a629e2ff867b240 http://data.gdeltproject.org/gdeltv2/20150218231500.export.CSV.zip',
     '339037 dec3f427076b716a8112b9086c342523 http://data.gdeltproject.org/gdeltv2/20150218231500.mentions.CSV.zip',
     '10269336 2f1a504a3c4558694ade0442e9a5ae6f http://data.gdeltproject.org/gdeltv2/20150218231500.gkg.csv.zip',
     '149723 12268e821823aae2da90882621feda18 http://data.gdeltproject.org/gdeltv2/20150218233000.export.CSV.zip',
     '357229 744acad14559f2781a8db67715d63872 http://data.gdeltproject.org/gdeltv2/20150218233000.mentions.CSV.zip',
     '11279827 66b03e2efd7d51dabf916b1666910053 http://data.gdeltproject.org/gdeltv2/20150218233000.gkg.csv.zip',
     '158842 a5298ce3c6df1a8a759c61b5c0b6f8bb http://data.gdeltproject.org/gdeltv2/20150218234500.export.CSV.zip',
     '374528 dd322c888f28311aca2c735468405551 http://data.gdeltproject.org/gdeltv2/20150218234500.mentions.CSV.zip',
     '11212939 cd20f295649b214dd16666ca451b9994 http://data.gdeltproject.org/gdeltv2/20150218234500.gkg.csv.zip',
     '362610 c4268d558bb22c02b3c132c17818c68b http://data.gdeltproject.org/gdeltv2/20150219000000.export.CSV.zip',
     '287807 e7f464a7a451ad2af6e9c8fa24f0ccea http://data.gdeltproject.org/gdeltv2/20150219000000.mentions.CSV.zip',
     '9728953 8f4b26e134bd6605cce2d32e92e5d3d7 http://data.gdeltproject.org/gdeltv2/20150219000000.gkg.csv.zip',
     '251605 7685a6c71f010918f3be0d4ed2be977e http://data.gdeltproject.org/gdeltv2/20150219001500.export.CSV.zip',
     '263793 e23ee65a60a1577dc74b979a54da406e http://data.gdeltproject.org/gdeltv2/20150219001500.mentions.CSV.zip',
     '9459370 6031464dfdcb331551d491916d400c18 http://data.gdeltproject.org/gdeltv2/20150219001500.gkg.csv.zip',
     '255259 f41066efb05d4024fca9dc1c2c6b9112 http://data.gdeltproject.org/gdeltv2/20150219003000.export.CSV.zip',
     '308019 061133d1efd29c66c7ecba0d52063927 http://data.gdeltproject.org/gdeltv2/20150219003000.mentions.CSV.zip',
     '10705358 84685f907404b79e7978a06a441b9731 http://data.gdeltproject.org/gdeltv2/20150219003000.gkg.csv.zip',
     '219398 555d808779fe5b3eaf0a9ebf212116a2 http://data.gdeltproject.org/gdeltv2/20150219004500.export.CSV.zip',
     '277207 0897fb7630ac913409c48345dca7565e http://data.gdeltproject.org/gdeltv2/20150219004500.mentions.CSV.zip',
     '9555639 b02920524f0b48c07bdab6c6d354a789 http://data.gdeltproject.org/gdeltv2/20150219004500.gkg.csv.zip',
     '225092 6b4e1d0421548dbba59754d0f164d2a1 http://data.gdeltproject.org/gdeltv2/20150219010000.export.CSV.zip',
     '286852 275a862fe0b27cdd3c3eabe2d05a964d http://data.gdeltproject.org/gdeltv2/20150219010000.mentions.CSV.zip',
     '9754826 5a84073aaf4a588319da7a53a83b56f1 http://data.gdeltproject.org/gdeltv2/20150219010000.gkg.csv.zip',
     '185226 36f14471b716d8b47c8f766507ab9adc http://data.gdeltproject.org/gdeltv2/20150219011500.export.CSV.zip',
     '268121 c9a62b0fdf05e4ae79a1ad1d9824af12 http://data.gdeltproject.org/gdeltv2/20150219011500.mentions.CSV.zip',
     '9014001 8862c82cb3fdfac53d98f658b7f369bf http://data.gdeltproject.org/gdeltv2/20150219011500.gkg.csv.zip',
     '175086 3da4bd2233db768a00affcf8bdecca90 http://data.gdeltproject.org/gdeltv2/20150219013000.export.CSV.zip',
     '256081 151ec7e83a35c91dcadeb7fe11dc0c6d http://data.gdeltproject.org/gdeltv2/20150219013000.mentions.CSV.zip',
     '8613269 5fab3a5da0b1f2ac368b93d17e206f35 http://data.gdeltproject.org/gdeltv2/20150219013000.gkg.csv.zip',
     '165120 79ee0ef2224af1e3d399d2ff377ec483 http://data.gdeltproject.org/gdeltv2/20150219014500.export.CSV.zip',
     '254277 8fb5f469d82575ce15049e982487aceb http://data.gdeltproject.org/gdeltv2/20150219014500.mentions.CSV.zip',
     '9002520 0270810b38cea1b1740e12b4e6390236 http://data.gdeltproject.org/gdeltv2/20150219014500.gkg.csv.zip',
     '156312 ef039d5a29019c7c52c6c3e4e0563d42 http://data.gdeltproject.org/gdeltv2/20150219020000.export.CSV.zip',
     '243548 9568632b94de04c3cbd627382ccd0abc http://data.gdeltproject.org/gdeltv2/20150219020000.mentions.CSV.zip',
     '8692622 7085497bbee05e76ec80ffd204d98f3a http://data.gdeltproject.org/gdeltv2/20150219020000.gkg.csv.zip',
     '184199 ee93accddff1014c71bbd49583f13d37 http://data.gdeltproject.org/gdeltv2/20150219021500.export.CSV.zip',
     '250721 d69b8e4c63aef45b6e33d57d9bfbf1ce http://data.gdeltproject.org/gdeltv2/20150219021500.mentions.CSV.zip',
     '8796798 d9877ebeeb92578998f96bf246c7afc2 http://data.gdeltproject.org/gdeltv2/20150219021500.gkg.csv.zip',
     '175103 f6a9149260de905b7afcb51c1c657d80 http://data.gdeltproject.org/gdeltv2/20150219023000.export.CSV.zip',
     '254741 1c0ba2869c68c7bbd2550accc32d108e http://data.gdeltproject.org/gdeltv2/20150219023000.mentions.CSV.zip',
     '8151815 e736d2cf5a7b5e827c26467adfea1d87 http://data.gdeltproject.org/gdeltv2/20150219023000.gkg.csv.zip',
     '148393 9cf4df7ab5b9ad23416b62ca93885d1a http://data.gdeltproject.org/gdeltv2/20150219024500.export.CSV.zip',
     '236600 7284631f4f7a9e66e1f34cacf6a51b44 http://data.gdeltproject.org/gdeltv2/20150219024500.mentions.CSV.zip',
     '8266363 2c4c5b08b90de1d385f46b9b972c2142 http://data.gdeltproject.org/gdeltv2/20150219024500.gkg.csv.zip',
     '119764 4361333ea8414e582f275a3aff150abe http://data.gdeltproject.org/gdeltv2/20150219030000.export.CSV.zip',
     '194510 8735ac4d5b55c4f4b1378af27d1aa95b http://data.gdeltproject.org/gdeltv2/20150219030000.mentions.CSV.zip',
     '7084391 30103f5209c5326744fe1c8bbf3a2dda http://data.gdeltproject.org/gdeltv2/20150219030000.gkg.csv.zip',
     '116897 7a6ac192edbbb268f5b97d1a652f078e http://data.gdeltproject.org/gdeltv2/20150219031500.export.CSV.zip',
     '184066 a8cc7055719167c7afe8d09499a721ed http://data.gdeltproject.org/gdeltv2/20150219031500.mentions.CSV.zip',
     '6038793 fc46678581951342fc28ab6a14f109a9 http://data.gdeltproject.org/gdeltv2/20150219031500.gkg.csv.zip',
     '144522 f5d93a40b313123c467719b52b66433e http://data.gdeltproject.org/gdeltv2/20150219033000.export.CSV.zip',
     '223190 0b8a8841ec47bbc4b3eb9c3b3f288c8e http://data.gdeltproject.org/gdeltv2/20150219033000.mentions.CSV.zip',
     '7847742 29be7c8f5f756f2bd3f02a96a80ed436 http://data.gdeltproject.org/gdeltv2/20150219033000.gkg.csv.zip',
     '133277 554362f119eb1edc73f0124bcb1d2f4d http://data.gdeltproject.org/gdeltv2/20150219040000.export.CSV.zip',
     '208145 db789cf9ca295b4e211c4d0b724d2e95 http://data.gdeltproject.org/gdeltv2/20150219040000.mentions.CSV.zip',
     '7061485 4314b3bb6e31b932eff3c9cd2a2ee677 http://data.gdeltproject.org/gdeltv2/20150219040000.gkg.csv.zip',
     '132912 cd7ee64d837d2540346ce4ba52a46545 http://data.gdeltproject.org/gdeltv2/20150219034500.export.CSV.zip',
     '215464 4d0898f98e1e8c59dfed048a60ab6750 http://data.gdeltproject.org/gdeltv2/20150219034500.mentions.CSV.zip',
     '7483233 580049907c162f5f0008cfd82b433bae http://data.gdeltproject.org/gdeltv2/20150219034500.gkg.csv.zip',
     '110116 760fbc79284b9c8dcae6bd493c2af24d http://data.gdeltproject.org/gdeltv2/20150219041500.export.CSV.zip',
     '194871 5a5d8d135b1e12f6d5299e48fdd871a8 http://data.gdeltproject.org/gdeltv2/20150219041500.mentions.CSV.zip',
     '6865435 ead6d92c03efd6c1fe8b631c09b7805b http://data.gdeltproject.org/gdeltv2/20150219041500.gkg.csv.zip',
     '101600 b5edf3092db1dd745013dd867128011b http://data.gdeltproject.org/gdeltv2/20150219043000.export.CSV.zip',
     '194383 097c9569993d97ad893c9c2b9525d1ee http://data.gdeltproject.org/gdeltv2/20150219043000.mentions.CSV.zip',
     '7135805 f0f5e7b56b35e2ef1790ebf46eaafb66 http://data.gdeltproject.org/gdeltv2/20150219043000.gkg.csv.zip',
     '127035 b8ae911ccb2b7ed70cd5d6863e8df397 http://data.gdeltproject.org/gdeltv2/20150219044500.export.CSV.zip',
     '198817 092d5fceb5f3059a4a512356255f1937 http://data.gdeltproject.org/gdeltv2/20150219044500.mentions.CSV.zip',
     '7208162 e7961bfcc7960f6348b4710fdecbbf58 http://data.gdeltproject.org/gdeltv2/20150219044500.gkg.csv.zip',
     '113155 9ab4b7cadce678e61d1acaf015b7cf59 http://data.gdeltproject.org/gdeltv2/20150219050000.export.CSV.zip',
     '189029 6491600e3653c5bf26ccbf0789933bfa http://data.gdeltproject.org/gdeltv2/20150219050000.mentions.CSV.zip',
     '6844933 df15d8ee4e8c912c981b3f94ed4a07c4 http://data.gdeltproject.org/gdeltv2/20150219050000.gkg.csv.zip',
     '104689 336ec8b697274ed103991dcc0bcbbd1d http://data.gdeltproject.org/gdeltv2/20150219051500.export.CSV.zip',
     '179096 5a3c751c24bbc6eac2e9f7afea372147 http://data.gdeltproject.org/gdeltv2/20150219051500.mentions.CSV.zip',
     '6643541 c285a920de038674cb0a6a752ca014d4 http://data.gdeltproject.org/gdeltv2/20150219051500.gkg.csv.zip',
     '164201 da49db31af0cd9d85300e7115d4e124b http://data.gdeltproject.org/gdeltv2/20150219053000.export.CSV.zip',
     '257918 a91cdfbab2ee2f3906b807aa2aff4a54 http://data.gdeltproject.org/gdeltv2/20150219053000.mentions.CSV.zip',
     '8145993 690d8385e7665b96c1c857003204682e http://data.gdeltproject.org/gdeltv2/20150219053000.gkg.csv.zip',
     '130974 800eef0b5fc572653836500a9e96bb36 http://data.gdeltproject.org/gdeltv2/20150219054500.export.CSV.zip',
     '225588 ca39dea61c4130858a632906d67f8eb2 http://data.gdeltproject.org/gdeltv2/20150219054500.mentions.CSV.zip',
     '7766949 284c493b7f326ed0d217d0bf4eb90143 http://data.gdeltproject.org/gdeltv2/20150219054500.gkg.csv.zip',
     '114925 61faaf18a6d2d054fb6694546d589907 http://data.gdeltproject.org/gdeltv2/20150219060000.export.CSV.zip',
     '192761 90d039bbdd39716f69faa732f074cfd7 http://data.gdeltproject.org/gdeltv2/20150219060000.mentions.CSV.zip',
     '7239102 454b7617049e6d9e95e157ae7c96395c http://data.gdeltproject.org/gdeltv2/20150219060000.gkg.csv.zip',
     '89269 a81966536ea3caeeb34af71b6558bc96 http://data.gdeltproject.org/gdeltv2/20150219061500.export.CSV.zip',
     '171219 04e161a06724a5699186262b74e9dac3 http://data.gdeltproject.org/gdeltv2/20150219061500.mentions.CSV.zip',
     '6173086 8b0b3edffd009942e2f10200980c5627 http://data.gdeltproject.org/gdeltv2/20150219061500.gkg.csv.zip',
     '142683 43aac04dbc39fec1ca36b125ea19d4b2 http://data.gdeltproject.org/gdeltv2/20150219063000.export.CSV.zip',
     '254392 7ce90085a77709a47a49b68fff7c7563 http://data.gdeltproject.org/gdeltv2/20150219063000.mentions.CSV.zip',
     '8838229 dd3783ac91519aae0afe2a96bdc53c32 http://data.gdeltproject.org/gdeltv2/20150219063000.gkg.csv.zip',
     '104711 b884a32912362a44f1981e904e6075cb http://data.gdeltproject.org/gdeltv2/20150219064500.export.CSV.zip',
     '188076 c73856d9b41c3a3f109609c251104095 http://data.gdeltproject.org/gdeltv2/20150219064500.mentions.CSV.zip',
     '6831637 a8b2e53b332b52b8239cc0a25cf70ec3 http://data.gdeltproject.org/gdeltv2/20150219064500.gkg.csv.zip',
     '401 10e9da91a8637b4dff1afa27943a3875 http://data.gdeltproject.org/gdeltv2/20150219071500.export.CSV.zip',
     '325 2fe7a04da89b1b73f32b3f170eb41e07 http://data.gdeltproject.org/gdeltv2/20150219071500.mentions.CSV.zip',
     '4311 34319caccb03fac244b8b66aa2ab9a27 http://data.gdeltproject.org/gdeltv2/20150219071500.gkg.csv.zip',
     '17661 f9e4b49dabd46678aa2fb91e57a0c958 http://data.gdeltproject.org/gdeltv2/20150219074500.export.CSV.zip',
     '15055 c1dcbcff2fe3b6e090962f8479c1e4fd http://data.gdeltproject.org/gdeltv2/20150219074500.mentions.CSV.zip',
     '618971 7a1bb74f913b6581b746f4459ae86eff http://data.gdeltproject.org/gdeltv2/20150219074500.gkg.csv.zip',
     '699 c772f500f8e4005af4267984806dea4d http://data.gdeltproject.org/gdeltv2/20150219080000.export.CSV.zip',
     '419 541a59c07a0b0828376edc018f0e96c1 http://data.gdeltproject.org/gdeltv2/20150219080000.mentions.CSV.zip',
     '7175 ab792df4f237fd09db339c10081f9fdd http://data.gdeltproject.org/gdeltv2/20150219080000.gkg.csv.zip',
     '1255680 1d51a5e0735186d5258e2cbdb230afc6 http://data.gdeltproject.org/gdeltv2/20150219093000.export.CSV.zip',
     '1945980 fed1f136123408afc30ec2a96f33f032 http://data.gdeltproject.org/gdeltv2/20150219093000.mentions.CSV.zip',
     '44538785 9c4dc7e48365091f1b764fae938f0993 http://data.gdeltproject.org/gdeltv2/20150219093000.gkg.csv.zip',
     '205250 8c310af2e4e6e08f00db3bf44dba4a07 http://data.gdeltproject.org/gdeltv2/20150219094500.export.CSV.zip',
     '387760 5a7e57b1d9e81f111b3dec7534133d49 http://data.gdeltproject.org/gdeltv2/20150219094500.mentions.CSV.zip',
     '194 26cad055aac9a78760e1daa1efa089b6 http://data.gdeltproject.org/gdeltv2/20150219094500.gkg.csv.zip',
     '220249 288a6f285839dd0f2f71fc9af75746e8 http://data.gdeltproject.org/gdeltv2/20150219101500.export.CSV.zip',
     '391438 db0859fdf1bb4dfc46a3b63016738fcb http://data.gdeltproject.org/gdeltv2/20150219101500.mentions.CSV.zip',
     '13099996 8759593c53127d2b97de916514938131 http://data.gdeltproject.org/gdeltv2/20150219101500.gkg.csv.zip',
     '107536 e86ee4f86eef3182f543429fd63f545d http://data.gdeltproject.org/gdeltv2/20150219103000.export.CSV.zip',
     '209271 f2c02e69e0c09eb979013f2db8dd0e83 http://data.gdeltproject.org/gdeltv2/20150219103000.mentions.CSV.zip',
     '7463154 18f2eee2aa82b028c6fab9224b6609e6 http://data.gdeltproject.org/gdeltv2/20150219103000.gkg.csv.zip',
     '119864 3eafeaa2fb80cd2200b7bad671bc2fb7 http://data.gdeltproject.org/gdeltv2/20150219104500.export.CSV.zip',
     '218684 c838b692b3f8e7e9ea286284d3eb78dd http://data.gdeltproject.org/gdeltv2/20150219104500.mentions.CSV.zip',
     '7225614 b5d7030fa4407e79800fe267c059046c http://data.gdeltproject.org/gdeltv2/20150219104500.gkg.csv.zip',
     '135165 b4933e4d178518aacb15077cf0d5d53f http://data.gdeltproject.org/gdeltv2/20150219110000.export.CSV.zip',
     '250481 eb3a8213f48a42d1ecfc6ffbba0b66cb http://data.gdeltproject.org/gdeltv2/20150219110000.mentions.CSV.zip',
     '7963826 df2285aa037beb9b905b6ce89cfcea7d http://data.gdeltproject.org/gdeltv2/20150219110000.gkg.csv.zip',
     '100746 b586f66e940ccd6ad0eff3710f345c49 http://data.gdeltproject.org/gdeltv2/20150219111500.export.CSV.zip',
     '179144 b738ea196319d100d4301b96d4359567 http://data.gdeltproject.org/gdeltv2/20150219111500.mentions.CSV.zip',
     '5828405 48b82c87d572bbe0cc16dee96edb838e http://data.gdeltproject.org/gdeltv2/20150219111500.gkg.csv.zip',
     '129564 d5f6eb2006ce76a92de9297379e072b9 http://data.gdeltproject.org/gdeltv2/20150219113000.export.CSV.zip',
     '209314 03e98e06c00ead57b99fda2c28a36917 http://data.gdeltproject.org/gdeltv2/20150219113000.mentions.CSV.zip',
     '7192749 56365c45d016669135305bafceaecd9b http://data.gdeltproject.org/gdeltv2/20150219113000.gkg.csv.zip',
     '120835 2d196ab1c7d373abd82efdb117256352 http://data.gdeltproject.org/gdeltv2/20150219114500.export.CSV.zip',
     '225915 f01c3c2dc32df7db772462001058de0b http://data.gdeltproject.org/gdeltv2/20150219114500.mentions.CSV.zip',
     '7634563 5bb2343c6371484deecf43c2946e16ed http://data.gdeltproject.org/gdeltv2/20150219114500.gkg.csv.zip',
     '119836 4d9d8235a24910ccb24f89fd85e932b8 http://data.gdeltproject.org/gdeltv2/20150219120000.export.CSV.zip',
     '204620 a814491a5d84e6c52801e45524dafd5f http://data.gdeltproject.org/gdeltv2/20150219120000.mentions.CSV.zip',
     '7028948 6bcff094c3aa0d7b02426a23e4369579 http://data.gdeltproject.org/gdeltv2/20150219120000.gkg.csv.zip',
     '89585 acb806ff5b5113a5d86b87c81af6109e http://data.gdeltproject.org/gdeltv2/20150219121500.export.CSV.zip',
     '163038 489442b5409ebe1075340d11f6b9e480 http://data.gdeltproject.org/gdeltv2/20150219121500.mentions.CSV.zip',
     '5867269 a487e0b873e0a17c9c9e9b2b4a3d5e14 http://data.gdeltproject.org/gdeltv2/20150219121500.gkg.csv.zip',
     '154902 56894bafbe7e8006659e084977ac8c78 http://data.gdeltproject.org/gdeltv2/20150219123000.export.CSV.zip',
     '252419 dc90380de047c150b2ce43d65314f5e4 http://data.gdeltproject.org/gdeltv2/20150219123000.mentions.CSV.zip',
     '8697412 2f51ff1c238a6403c5b740f4175e7e2f http://data.gdeltproject.org/gdeltv2/20150219123000.gkg.csv.zip',
     '131006 bbb56b34c14d1da59b834a82bf74bc2a http://data.gdeltproject.org/gdeltv2/20150219124500.export.CSV.zip',
     '228111 5226b93f0f874df270671379a2faa49a http://data.gdeltproject.org/gdeltv2/20150219124500.mentions.CSV.zip',
     '8190264 f3920bc3f78fcbe6099cb810a6fe4129 http://data.gdeltproject.org/gdeltv2/20150219124500.gkg.csv.zip',
     '108004 b4759fdbd3b7f793ea8b7705f694f62c http://data.gdeltproject.org/gdeltv2/20150219130000.export.CSV.zip',
     '192407 ffa56b07dfe82629ad80b2d7910fca0d http://data.gdeltproject.org/gdeltv2/20150219130000.mentions.CSV.zip',
     '7134704 4d5889af088b004b245c7f28e9468062 http://data.gdeltproject.org/gdeltv2/20150219130000.gkg.csv.zip',
     '134886 4183b478c5581495b920e205f333f6d1 http://data.gdeltproject.org/gdeltv2/20150219131500.export.CSV.zip',
     '257905 2381f6ba4780abde63496d0325d32a57 http://data.gdeltproject.org/gdeltv2/20150219131500.mentions.CSV.zip',
     '8747063 9aab3b1bd8f2d926171049465bf1ec76 http://data.gdeltproject.org/gdeltv2/20150219131500.gkg.csv.zip',
     '122144 0426364fee3f76a32f072effbfcc272d http://data.gdeltproject.org/gdeltv2/20150219133000.export.CSV.zip',
     '222100 be6fe659f166292ffdb77ba460adc9b3 http://data.gdeltproject.org/gdeltv2/20150219133000.mentions.CSV.zip',
     '8527034 f46feeb8d1970473234126cc4c5d3a37 http://data.gdeltproject.org/gdeltv2/20150219133000.gkg.csv.zip',
     '152104 0bdff8ec2ad96a35ecbd6682f82b6c57 http://data.gdeltproject.org/gdeltv2/20150219134500.export.CSV.zip',
     '280227 ca5ff302248b2eb3d78352d5c09eafd1 http://data.gdeltproject.org/gdeltv2/20150219134500.mentions.CSV.zip',
     '9921299 4c78969eca5c35367f1853ba546396e1 http://data.gdeltproject.org/gdeltv2/20150219134500.gkg.csv.zip',
     '214619 d2edc91aa30db7c0bc80ad716bf82465 http://data.gdeltproject.org/gdeltv2/20150219140000.export.CSV.zip',
     '378571 912e15af0d9a2055e2c62f99ac2320df http://data.gdeltproject.org/gdeltv2/20150219140000.mentions.CSV.zip',
     '13669981 884eb91ebd44f6815844734f19f90a9a http://data.gdeltproject.org/gdeltv2/20150219140000.gkg.csv.zip',
     '197503 dd8645b796437495ea8a00fef1266abf http://data.gdeltproject.org/gdeltv2/20150219141500.export.CSV.zip',
     '369507 eff417e8a05836cc969fa0fab7e8de19 http://data.gdeltproject.org/gdeltv2/20150219141500.mentions.CSV.zip',
     '14217868 a96ad6e2b3e3715561294f1d572c148e http://data.gdeltproject.org/gdeltv2/20150219141500.gkg.csv.zip',
     '229421 862edf0a22f7bf24bd882cc6eaa0ffad http://data.gdeltproject.org/gdeltv2/20150219143000.export.CSV.zip',
     '410881 da9d10ec5ee8e9462c2fe2882d16aa9d http://data.gdeltproject.org/gdeltv2/20150219143000.mentions.CSV.zip',
     '16172186 14b7f8a104cd37c6e5441a5ff8d695dc http://data.gdeltproject.org/gdeltv2/20150219143000.gkg.csv.zip',
     '171509 a093ad8ead656befe486586e27ee5991 http://data.gdeltproject.org/gdeltv2/20150219144500.export.CSV.zip',
     '332574 693c9ad88596adc6f02b89944b1b28f3 http://data.gdeltproject.org/gdeltv2/20150219144500.mentions.CSV.zip',
     '12178916 6775f42fcc8f080e28d8a58eca86393b http://data.gdeltproject.org/gdeltv2/20150219144500.gkg.csv.zip',
     '154693 9b054c762585f9865b1ecd2c493854b3 http://data.gdeltproject.org/gdeltv2/20150219150000.export.CSV.zip',
     '279837 63e52561a165e5d9326170ec277e28ee http://data.gdeltproject.org/gdeltv2/20150219150000.mentions.CSV.zip',
     '9351772 1ec221cd30310f8044d319dc17ab161d http://data.gdeltproject.org/gdeltv2/20150219150000.gkg.csv.zip',
     '150922 158af0d979398d8ee18b1bcbceee6011 http://data.gdeltproject.org/gdeltv2/20150219151500.export.CSV.zip',
     '296332 11c570e9a5b56aace61e58052f21bdcb http://data.gdeltproject.org/gdeltv2/20150219151500.mentions.CSV.zip',
     '10642084 3dd2c8f6ee81e95acf16d98d3c4a6a0a http://data.gdeltproject.org/gdeltv2/20150219151500.gkg.csv.zip',
     '165418 8b9a2fd4d35c50d1f99154d3c1ba84a3 http://data.gdeltproject.org/gdeltv2/20150219153000.export.CSV.zip',
     '310341 ad4ee59896367d67254ac4193a85ca52 http://data.gdeltproject.org/gdeltv2/20150219153000.mentions.CSV.zip',
     '10788997 fb35fe05f5d63aa81ec89109c8673941 http://data.gdeltproject.org/gdeltv2/20150219153000.gkg.csv.zip',
     '151096 7bce2f22c7f6199b8211cbf6e2a582b2 http://data.gdeltproject.org/gdeltv2/20150219154500.export.CSV.zip',
     '242516 6a7607f93477acc0e08be557a5a56e4d http://data.gdeltproject.org/gdeltv2/20150219154500.mentions.CSV.zip',
     '8990428 1de1935518de5bac768d43ae04c8ccd9 http://data.gdeltproject.org/gdeltv2/20150219154500.gkg.csv.zip',
     '152515 8bfbac919e94ab0596fea5d8d54b078c http://data.gdeltproject.org/gdeltv2/20150219160000.export.CSV.zip',
     '274210 4840c8ba17ea3237a3b29e0861fe9b98 http://data.gdeltproject.org/gdeltv2/20150219160000.mentions.CSV.zip',
     '9272076 3ef583c3b6b50b08f0e1f6afa928e702 http://data.gdeltproject.org/gdeltv2/20150219160000.gkg.csv.zip',
     '171331 8bd79c9c5ad071c7f1bdbb8616645fef http://data.gdeltproject.org/gdeltv2/20150219161500.export.CSV.zip',
     '338009 7b376006c5960e53703c24b87a5fe94a http://data.gdeltproject.org/gdeltv2/20150219161500.mentions.CSV.zip',
     '11663807 3fcb4b3b9bb302cbdec99cfcc30ea935 http://data.gdeltproject.org/gdeltv2/20150219161500.gkg.csv.zip',
     '172045 6d108997d816ea14af26605ac8bdd8fe http://data.gdeltproject.org/gdeltv2/20150219163000.export.CSV.zip',
     '297042 fe3acfa1778b7561efac6189d8e2b4fe http://data.gdeltproject.org/gdeltv2/20150219163000.mentions.CSV.zip',
     '9419170 0268a043db3380b3cfb4248557f7eafa http://data.gdeltproject.org/gdeltv2/20150219163000.gkg.csv.zip',
     '169471 ee4b2bb27ceb9f7f3f662efc72bf6c92 http://data.gdeltproject.org/gdeltv2/20150219164500.export.CSV.zip',
     '294372 2c4b6f43ea6e53db1adc744a85ac8172 http://data.gdeltproject.org/gdeltv2/20150219164500.mentions.CSV.zip',
     '9566002 d45d0cf88cc307e1aeb32757e175912c http://data.gdeltproject.org/gdeltv2/20150219164500.gkg.csv.zip',
     '186608 93d66cde9b1cdb66a2d2fda7c57513a0 http://data.gdeltproject.org/gdeltv2/20150219170000.export.CSV.zip',
     '319847 f8d0fcb922ac908eb1d7f21ee734253f http://data.gdeltproject.org/gdeltv2/20150219170000.mentions.CSV.zip',
     '10628387 d1a49fe280adb61e46214eb7a6ab3912 http://data.gdeltproject.org/gdeltv2/20150219170000.gkg.csv.zip',
     '169201 7da87b8386dfef937f41e5f034b766b5 http://data.gdeltproject.org/gdeltv2/20150219171500.export.CSV.zip',
     '296484 ad535f1cac65064e940438bcc5041913 http://data.gdeltproject.org/gdeltv2/20150219171500.mentions.CSV.zip',
     '9407953 78755d3929bf3f065f721afd942d5300 http://data.gdeltproject.org/gdeltv2/20150219171500.gkg.csv.zip',
     '158811 8c335e859781b0c77daf5d52bd544bcd http://data.gdeltproject.org/gdeltv2/20150219173000.export.CSV.zip',
     '310478 daaaee0803bd54ce53e779620090a01f http://data.gdeltproject.org/gdeltv2/20150219173000.mentions.CSV.zip',
     '9648477 534c48d1b0b400a3ce96baa3db796dbb http://data.gdeltproject.org/gdeltv2/20150219173000.gkg.csv.zip',
     '184245 61c2b7590e17d153166c7e1715ac78dd http://data.gdeltproject.org/gdeltv2/20150219174500.export.CSV.zip',
     '346359 ed707339c69d21984f2b64bf4481e91b http://data.gdeltproject.org/gdeltv2/20150219174500.mentions.CSV.zip',
     '10931582 1fe902132a99cddec0a50058d156264e http://data.gdeltproject.org/gdeltv2/20150219174500.gkg.csv.zip',
     '94088 691be8988a4657f0e5500c100d89ccc8 http://data.gdeltproject.org/gdeltv2/20150219180000.export.CSV.zip',
     '177513 40cfdf8d3975fdb0da1424824ab753bf http://data.gdeltproject.org/gdeltv2/20150219180000.mentions.CSV.zip',
     '6432862 3f32aa302d712625d44ede0c76ea0ee3 http://data.gdeltproject.org/gdeltv2/20150219180000.gkg.csv.zip',
     '116195 eb168ccc8f1e02ff3a39b956cc303c63 http://data.gdeltproject.org/gdeltv2/20150219181500.export.CSV.zip',
     '228289 d9c1d2cc50336f7a47ddfcf301b3d138 http://data.gdeltproject.org/gdeltv2/20150219181500.mentions.CSV.zip',
     '8292707 bce233e039b0553177f32a1f282e34ae http://data.gdeltproject.org/gdeltv2/20150219181500.gkg.csv.zip',
     '203087 f7c58d99b1001ee19df66bf8be752d0e http://data.gdeltproject.org/gdeltv2/20150219183000.export.CSV.zip',
     '416566 82182f22be4615db00e711ced3d5f99e http://data.gdeltproject.org/gdeltv2/20150219183000.mentions.CSV.zip',
     '13220449 3bc196b092f07ae2aeacdc196c12698a http://data.gdeltproject.org/gdeltv2/20150219183000.gkg.csv.zip',
     '586756 b7190310a36b810fcb8fbd5f5eb5d237 http://data.gdeltproject.org/gdeltv2/20150219184500.export.CSV.zip',
     '796906 4c8f75ec34031a2cc77a4be232c687a4 http://data.gdeltproject.org/gdeltv2/20150219184500.mentions.CSV.zip',
     '31472956 368afe6cb27cb99b3d73e9317cbb5a73 http://data.gdeltproject.org/gdeltv2/20150219184500.gkg.csv.zip',
     '200450 3f5b0de73588b11473a71987f295ac94 http://data.gdeltproject.org/gdeltv2/20150219190000.export.CSV.zip',
     '382039 73b8cde4da8f144c0979b4c74b6b7070 http://data.gdeltproject.org/gdeltv2/20150219190000.mentions.CSV.zip',
     '13384659 c54fc539a27b966928b00148cdeb20b4 http://data.gdeltproject.org/gdeltv2/20150219190000.gkg.csv.zip',
     '244613 e6e93e5e7c99c14368f8da5e9807bf90 http://data.gdeltproject.org/gdeltv2/20150219191500.export.CSV.zip',
     '468141 eb32f0f0d35820cf09b2263f20248612 http://data.gdeltproject.org/gdeltv2/20150219191500.mentions.CSV.zip',
     '17678147 4fb5ebd71d0d69e3099fab25500f3d77 http://data.gdeltproject.org/gdeltv2/20150219191500.gkg.csv.zip',
     '170750 b56111bc8e9bf418d548c106eb78b2ab http://data.gdeltproject.org/gdeltv2/20150219193000.export.CSV.zip',
     '355165 a5f60bda3bdf1faf62e3e9da3ed2c98f http://data.gdeltproject.org/gdeltv2/20150219193000.mentions.CSV.zip',
     '13090374 b848f91377faa19f7c4f9f5e15e86b35 http://data.gdeltproject.org/gdeltv2/20150219193000.gkg.csv.zip',
     '144328 a920ae807312b8790be0ef443aa198ce http://data.gdeltproject.org/gdeltv2/20150219194500.export.CSV.zip',
     '264836 8b33707a5be3fdbec995106de2e20db2 http://data.gdeltproject.org/gdeltv2/20150219194500.mentions.CSV.zip',
     '9159262 ffc68d81d79c74870e78cf4ac0210f50 http://data.gdeltproject.org/gdeltv2/20150219194500.gkg.csv.zip',
     '162667 604acc5c4f1b80bc13e24ede1247efe5 http://data.gdeltproject.org/gdeltv2/20150219200000.export.CSV.zip',
     '390024 51d99c498b769353753b9e14777cfc5e http://data.gdeltproject.org/gdeltv2/20150219200000.mentions.CSV.zip',
     '13674647 553b7079b866b0afdcbf1540a04f0237 http://data.gdeltproject.org/gdeltv2/20150219200000.gkg.csv.zip',
     '137456 3278c4c535520f1de26617d697de2259 http://data.gdeltproject.org/gdeltv2/20150219201500.export.CSV.zip',
     '280877 127ba77e3583115f6f36dd940504b2b1 http://data.gdeltproject.org/gdeltv2/20150219201500.mentions.CSV.zip',
     '10091653 5f0441ecce793b920e38cafcd10368cd http://data.gdeltproject.org/gdeltv2/20150219201500.gkg.csv.zip',
     '134997 c5127df2e9d63edf2e4681d273ff9922 http://data.gdeltproject.org/gdeltv2/20150219203000.export.CSV.zip',
     '279019 b1c7dbf99142da6976333692673084a5 http://data.gdeltproject.org/gdeltv2/20150219203000.mentions.CSV.zip',
     '9044860 234de32e19a2fbe4c0cc575ca1a31aba http://data.gdeltproject.org/gdeltv2/20150219203000.gkg.csv.zip',
     '150194 622b72ef99bf59436edb0dd6a20a47ee http://data.gdeltproject.org/gdeltv2/20150219204500.export.CSV.zip',
     '311290 606437a1b85525dd632d61919c6759d7 http://data.gdeltproject.org/gdeltv2/20150219204500.mentions.CSV.zip',
     '11171491 a731aef13afe1026ea29f8aee5a2192e http://data.gdeltproject.org/gdeltv2/20150219204500.gkg.csv.zip',
     '134114 963e0773d7873b2bb6e843b102405c8a http://data.gdeltproject.org/gdeltv2/20150219210000.export.CSV.zip',
     '283487 4619e9c5d336aa0938af70f9a45da5dd http://data.gdeltproject.org/gdeltv2/20150219210000.mentions.CSV.zip',
     '10108395 985701ec81e96c1200dcc70a560080cb http://data.gdeltproject.org/gdeltv2/20150219210000.gkg.csv.zip',
     '96651 9d0adcc895c49a0a63806d3928842127 http://data.gdeltproject.org/gdeltv2/20150219211500.export.CSV.zip',
     '161412 14f0e864ab808a36c577f4e5c282c7c0 http://data.gdeltproject.org/gdeltv2/20150219211500.mentions.CSV.zip',
     '5013330 c77e0361f41ea2780594d481c598c13f http://data.gdeltproject.org/gdeltv2/20150219211500.gkg.csv.zip',
     '152177 ea010de95f0970dacfd0f41eea72e48d http://data.gdeltproject.org/gdeltv2/20150219213000.export.CSV.zip',
     '329607 14bec8de6349d5b80a2a3df848096713 http://data.gdeltproject.org/gdeltv2/20150219213000.mentions.CSV.zip',
     '10660248 19ca35db73a124d21d269ab1d686a202 http://data.gdeltproject.org/gdeltv2/20150219213000.gkg.csv.zip',
     '113536 421010c7af41705b7b6e044b0008c671 http://data.gdeltproject.org/gdeltv2/20150219214500.export.CSV.zip',
     '258799 3e6e202c1ad196c9ebd5902ac354e46d http://data.gdeltproject.org/gdeltv2/20150219214500.mentions.CSV.zip',
     '8889686 8c5f49038182d238af6fb3e10cbc600c http://data.gdeltproject.org/gdeltv2/20150219214500.gkg.csv.zip',
     '116346 88a0e7be5e8f5cdf434e15f3dfd9ee73 http://data.gdeltproject.org/gdeltv2/20150219220000.export.CSV.zip',
     '250745 11f4f15391c2e86ca9ed7fdf17394f27 http://data.gdeltproject.org/gdeltv2/20150219220000.mentions.CSV.zip',
     '9028660 c7310263922c71c9c18999bf2896488b http://data.gdeltproject.org/gdeltv2/20150219220000.gkg.csv.zip',
     '146511 c2f29903767caf9a0d43fc4599cbb9be http://data.gdeltproject.org/gdeltv2/20150219221500.export.CSV.zip',
     '287882 1ad8f01e0a8fb951a3ee3af99ddbe556 http://data.gdeltproject.org/gdeltv2/20150219221500.mentions.CSV.zip',
     '9670010 467e826b09e1b515e1b7a400fe084ed8 http://data.gdeltproject.org/gdeltv2/20150219221500.gkg.csv.zip',
     '148807 edafa0426e139babdf7c19bf3587deba http://data.gdeltproject.org/gdeltv2/20150219223000.export.CSV.zip',
     '293274 ce8cd68d2a6a98e399d3cc281c2b2c32 http://data.gdeltproject.org/gdeltv2/20150219223000.mentions.CSV.zip',
     '9216902 8afdea195eb32b7ef392456832c907e1 http://data.gdeltproject.org/gdeltv2/20150219223000.gkg.csv.zip',
     '105220 d8034a9c44ccf0aef6e44e61bf0f3e84 http://data.gdeltproject.org/gdeltv2/20150219224500.export.CSV.zip',
     '213532 1294d232f21056ea14f0fadfc5cce50b http://data.gdeltproject.org/gdeltv2/20150219224500.mentions.CSV.zip',
     '7416249 9589707634a15acc5f3d4e9e63d5f3f7 http://data.gdeltproject.org/gdeltv2/20150219224500.gkg.csv.zip',
     '159613 a6a9fe2299b0c33d840029aa62c6533a http://data.gdeltproject.org/gdeltv2/20150219230000.export.CSV.zip',
     '362865 af65df88cd807467df7cb3ab5c48dc07 http://data.gdeltproject.org/gdeltv2/20150219230000.mentions.CSV.zip',
     '12795456 469099ee5fcc03fe76b6935d39ef6489 http://data.gdeltproject.org/gdeltv2/20150219230000.gkg.csv.zip',
     '146892 b6298791f117f06fb48fef65aadf7c30 http://data.gdeltproject.org/gdeltv2/20150219231500.export.CSV.zip',
     '323577 00a5211a4344dfe3528e4c1604558025 http://data.gdeltproject.org/gdeltv2/20150219231500.mentions.CSV.zip',
     '10345004 e38a5ce20a7ac1f18f774246eabd7706 http://data.gdeltproject.org/gdeltv2/20150219231500.gkg.csv.zip',
     '144433 b182d0acd8e73a818f77f1731f1bdac4 http://data.gdeltproject.org/gdeltv2/20150219233000.export.CSV.zip',
     '266529 03c0a3df9ee340f28118036f0ad8619d http://data.gdeltproject.org/gdeltv2/20150219233000.mentions.CSV.zip',
     '9176890 0cab82f9aca61ff946f750d099f0c2f7 http://data.gdeltproject.org/gdeltv2/20150219233000.gkg.csv.zip',
     '183037 748cc594a9b9951d8cfeddc9ad54ae40 http://data.gdeltproject.org/gdeltv2/20150219234500.export.CSV.zip',
     '446199 7b39caba9c9afa46da2a30199173dd84 http://data.gdeltproject.org/gdeltv2/20150219234500.mentions.CSV.zip',
     '16480049 1dc31a0ea4412446ccd6d39cd86d8c1a http://data.gdeltproject.org/gdeltv2/20150219234500.gkg.csv.zip',
     '364303 84f74d879d587675fcd49ca89c1e7341 http://data.gdeltproject.org/gdeltv2/20150220000000.export.CSV.zip',
     '285959 41cfeba353f2a962eae7231e9c9c68ce http://data.gdeltproject.org/gdeltv2/20150220000000.mentions.CSV.zip',
     '11452590 86cf6ad7153c9d136999a1d473adb2b1 http://data.gdeltproject.org/gdeltv2/20150220000000.gkg.csv.zip',
     '296880 4e94b5a50581de62b99c17ebff3f64ce http://data.gdeltproject.org/gdeltv2/20150220001500.export.CSV.zip',
     '298441 37ac99132da80ec6ddec405b7e58fd12 http://data.gdeltproject.org/gdeltv2/20150220001500.mentions.CSV.zip',
     '10682642 434cda477d8ba92e042b29a6eb0bbe74 http://data.gdeltproject.org/gdeltv2/20150220001500.gkg.csv.zip',
     '303209 77502fbb6a7b7d4adac1c69ecac974bd http://data.gdeltproject.org/gdeltv2/20150220003000.export.CSV.zip',
     '340742 8f24c6d981eb485671d130421074eed3 http://data.gdeltproject.org/gdeltv2/20150220003000.mentions.CSV.zip',
     '12789481 1fcf69cee9ede948de0ff55b8d35e53d http://data.gdeltproject.org/gdeltv2/20150220003000.gkg.csv.zip',
     '220130 f840f71e994716a5d387e8be23fc60e4 http://data.gdeltproject.org/gdeltv2/20150220004500.export.CSV.zip',
     '265154 0783a8c915c9bbc0656afa3176d32de9 http://data.gdeltproject.org/gdeltv2/20150220004500.mentions.CSV.zip',
     '9062539 c6b047a0ddc70ef3e6c094cb82f17683 http://data.gdeltproject.org/gdeltv2/20150220004500.gkg.csv.zip',
     '187244 9199838e7574a5c3beea8560faddfe7a http://data.gdeltproject.org/gdeltv2/20150220010000.export.CSV.zip',
     '235001 9331c180bc20b282ff87f2f2354e06a8 http://data.gdeltproject.org/gdeltv2/20150220010000.mentions.CSV.zip',
     '8390132 e7c679ceaa294a67640dc35415ffad51 http://data.gdeltproject.org/gdeltv2/20150220010000.gkg.csv.zip',
     '186261 14b906a8cca1625da1dd8fd4265bdddb http://data.gdeltproject.org/gdeltv2/20150220011500.export.CSV.zip',
     '257239 f3d62056e980dda4fdc32e1a7a0bb14a http://data.gdeltproject.org/gdeltv2/20150220011500.mentions.CSV.zip',
     '8599105 c5a4af0365e9d3d815849ea38bace66e http://data.gdeltproject.org/gdeltv2/20150220011500.gkg.csv.zip',
     '147608 e6e97dde8fd5215a8bfce174397a1008 http://data.gdeltproject.org/gdeltv2/20150220013000.export.CSV.zip',
     '197940 7d2243932269b971cdc0124cf1244abc http://data.gdeltproject.org/gdeltv2/20150220013000.mentions.CSV.zip',
     '7273467 ff77bacbf26f5820cd03b5965bc37a9f http://data.gdeltproject.org/gdeltv2/20150220013000.gkg.csv.zip',
     '138471 415cb540ff78d6dc46137c59a3ccee31 http://data.gdeltproject.org/gdeltv2/20150220014500.export.CSV.zip',
     '196463 a98e09d3f04c45d4a83af4e1f92a056d http://data.gdeltproject.org/gdeltv2/20150220014500.mentions.CSV.zip',
     '7064876 affcc7df0c10c7e995cd01ba669154aa http://data.gdeltproject.org/gdeltv2/20150220014500.gkg.csv.zip',
     '139625 40b2bd24864c9d86ef7045178cc572c9 http://data.gdeltproject.org/gdeltv2/20150220020000.export.CSV.zip',
     '208318 289a911e3f2c208d34039dc175d5815a http://data.gdeltproject.org/gdeltv2/20150220020000.mentions.CSV.zip',
     '7766924 82e66be18368a53e5bc4057bc69de544 http://data.gdeltproject.org/gdeltv2/20150220020000.gkg.csv.zip',
     '135642 564b121e0399d97e08e43d4258e72269 http://data.gdeltproject.org/gdeltv2/20150220021500.export.CSV.zip',
     '195487 662bd27a3453301f32aaf9bbc36b8433 http://data.gdeltproject.org/gdeltv2/20150220021500.mentions.CSV.zip',
     '6547313 f5090ba287873c61f54804fc10081944 http://data.gdeltproject.org/gdeltv2/20150220021500.gkg.csv.zip',
     '119588 f0bcb267a7d1fcb3c41f42679b2e280d http://data.gdeltproject.org/gdeltv2/20150220023000.export.CSV.zip',
     '168843 de6aedd45877364bbb4397a2b4b24f70 http://data.gdeltproject.org/gdeltv2/20150220023000.mentions.CSV.zip',
     '5705469 0dca2a09330c37d248797ad0a5205e67 http://data.gdeltproject.org/gdeltv2/20150220023000.gkg.csv.zip',
     '132087 2e37daea2210e316c4dabf323b782f68 http://data.gdeltproject.org/gdeltv2/20150220024500.export.CSV.zip',
     '202436 ba1eb605e705b3583c550206964b6538 http://data.gdeltproject.org/gdeltv2/20150220024500.mentions.CSV.zip',
     '6951110 4c11fffd9ed76544beb6f8646fb6fc64 http://data.gdeltproject.org/gdeltv2/20150220024500.gkg.csv.zip',
     '132245 4ca1e974547d58e0f27421eacc51c3d0 http://data.gdeltproject.org/gdeltv2/20150220030000.export.CSV.zip',
     '166368 3eb4c86a8f9d9eb46655795ec5b7a622 http://data.gdeltproject.org/gdeltv2/20150220030000.mentions.CSV.zip',
     '6235926 e7890ee86ade895029c401b0f517abf9 http://data.gdeltproject.org/gdeltv2/20150220030000.gkg.csv.zip',
     '112374 c8a831a3a456ecf4dd12938bbbb02e02 http://data.gdeltproject.org/gdeltv2/20150220033000.export.CSV.zip',
     '182206 0eecfa1851d9218c89a4da4f4c8a8302 http://data.gdeltproject.org/gdeltv2/20150220033000.mentions.CSV.zip',
     '6894350 f576e2ece605c44026272b88e2a1f0a8 http://data.gdeltproject.org/gdeltv2/20150220033000.gkg.csv.zip',
     '85132 b591571de0fe32e5edbea5006ad3404d http://data.gdeltproject.org/gdeltv2/20150220031500.export.CSV.zip',
     '131790 a0b423fbc238f63fadafafbea319a1a8 http://data.gdeltproject.org/gdeltv2/20150220031500.mentions.CSV.zip',
     '4918537 30c791ed843e22d1323a71f1c97557f6 http://data.gdeltproject.org/gdeltv2/20150220031500.gkg.csv.zip',
     '97861 dbbde866b2aa750d125f22ce7cd6dbba http://data.gdeltproject.org/gdeltv2/20150220034500.export.CSV.zip',
     '148800 c00b8c769b2f3e51fcb85f770b97d023 http://data.gdeltproject.org/gdeltv2/20150220034500.mentions.CSV.zip',
     '5739270 be9d5241e162ab890c34ec66e69d59ad http://data.gdeltproject.org/gdeltv2/20150220034500.gkg.csv.zip',
     '147301 1f3c398aaf6b698cba1165a3c5e83d5a http://data.gdeltproject.org/gdeltv2/20150220040000.export.CSV.zip',
     '229130 04125579ec0c2f07c7d0db9b6b1c48a3 http://data.gdeltproject.org/gdeltv2/20150220040000.mentions.CSV.zip',
     '9069016 03e876e48a5d288b3c30424ec7691341 http://data.gdeltproject.org/gdeltv2/20150220040000.gkg.csv.zip',
     '171010 ad2db0dc075cb6226a12bab6c3021b61 http://data.gdeltproject.org/gdeltv2/20150220041500.export.CSV.zip',
     '244754 abd2d797ee79b4ee36af0b3c736a6e7c http://data.gdeltproject.org/gdeltv2/20150220041500.mentions.CSV.zip',
     '9130695 c8ed36b185a7f590ac4618097a381a19 http://data.gdeltproject.org/gdeltv2/20150220041500.gkg.csv.zip',
     '145630 e5b8e061b83437f5b7fe6db12918201b http://data.gdeltproject.org/gdeltv2/20150220043000.export.CSV.zip',
     '214964 328ba0673f6a90bd32d615d5eb610bfc http://data.gdeltproject.org/gdeltv2/20150220043000.mentions.CSV.zip',
     '7989206 e789b2ddecfc96145dbdcd0a3228ce79 http://data.gdeltproject.org/gdeltv2/20150220043000.gkg.csv.zip',
     '143812 0cbfe8e41c5b0a691a6ac274921f05d9 http://data.gdeltproject.org/gdeltv2/20150220044500.export.CSV.zip',
     '218414 e35140523e94d59b3c19aeb7b8704ebf http://data.gdeltproject.org/gdeltv2/20150220044500.mentions.CSV.zip',
     '8840237 ab8fc59d6b5e5414f5a2d12cd1dd9aff http://data.gdeltproject.org/gdeltv2/20150220044500.gkg.csv.zip',
     '130809 feaea519de9ee80d4f9269e2f16a9bf7 http://data.gdeltproject.org/gdeltv2/20150220050000.export.CSV.zip',
     '214295 86e6fa2437289f7453ef1a0a85dd8dd6 http://data.gdeltproject.org/gdeltv2/20150220050000.mentions.CSV.zip',
     '8918709 9b18bb995a8e2049f95e4ad783df30fc http://data.gdeltproject.org/gdeltv2/20150220050000.gkg.csv.zip',
     '122447 3b5b1df37a3426a6999b3ba73ec54577 http://data.gdeltproject.org/gdeltv2/20150220051500.export.CSV.zip',
     '176201 475d3b2197998d0d916ec5fdd08fb1bf http://data.gdeltproject.org/gdeltv2/20150220051500.mentions.CSV.zip',
     '6699550 4e1acbc94dd0754f0db050c49db4b8be http://data.gdeltproject.org/gdeltv2/20150220051500.gkg.csv.zip',
     '148448 307d4ff0130af384bac41827b744bf3b http://data.gdeltproject.org/gdeltv2/20150220053000.export.CSV.zip',
     '224157 93ea0f9b9ca049a629469b1d497b53df http://data.gdeltproject.org/gdeltv2/20150220053000.mentions.CSV.zip',
     '6942929 f128cf7f3b8fc511136598ddcb1a97db http://data.gdeltproject.org/gdeltv2/20150220053000.gkg.csv.zip',
     '123451 bf6fc821eb02a4223256dd227d4f6a23 http://data.gdeltproject.org/gdeltv2/20150220054500.export.CSV.zip',
     '227155 52db8dbf3eb90596c48c3383ceec0b1a http://data.gdeltproject.org/gdeltv2/20150220054500.mentions.CSV.zip',
     '7930766 8db9f34c8ad580527020f7142547da5e http://data.gdeltproject.org/gdeltv2/20150220054500.gkg.csv.zip',
     '107416 43c44576e0fa9b79909511e70eacb836 http://data.gdeltproject.org/gdeltv2/20150220060000.export.CSV.zip',
     '199774 d78ff2d03c080811cc969cbb7acaa7a4 http://data.gdeltproject.org/gdeltv2/20150220060000.mentions.CSV.zip',
     '7378740 d4a7284f22ecca31a2b00528646ec88c http://data.gdeltproject.org/gdeltv2/20150220060000.gkg.csv.zip',
     '103940 1a1b93a092c8b6c57c6b08bb0c622abc http://data.gdeltproject.org/gdeltv2/20150220061500.export.CSV.zip',
     '186463 a422f2c1e536a1b3d9a0176a11e96500 http://data.gdeltproject.org/gdeltv2/20150220061500.mentions.CSV.zip',
     '6846061 8022f2266077280e6d0d1c4849d03d32 http://data.gdeltproject.org/gdeltv2/20150220061500.gkg.csv.zip',
     '130478 f1ff349c86bda8932ed43b3221dcad3e http://data.gdeltproject.org/gdeltv2/20150220063000.export.CSV.zip',
     '199507 9f641b8b306b547c9eb01b67c442368a http://data.gdeltproject.org/gdeltv2/20150220063000.mentions.CSV.zip',
     '7315948 a076c36b7d39fb052dabd04912200c5e http://data.gdeltproject.org/gdeltv2/20150220063000.gkg.csv.zip',
     '134566 fc53283bc8ee6c41227629d02ace32d8 http://data.gdeltproject.org/gdeltv2/20150220064500.export.CSV.zip',
     '207699 5b05ca8f8724b1723fe71055e859ea90 http://data.gdeltproject.org/gdeltv2/20150220064500.mentions.CSV.zip',
     '7062871 e53bb8fa3d5ccddb9dcfd28cae1124d0 http://data.gdeltproject.org/gdeltv2/20150220064500.gkg.csv.zip',
     '82520 37ae9ca15c12458ef5a2eef1a92d658d http://data.gdeltproject.org/gdeltv2/20150220070000.export.CSV.zip',
     '147404 3b2761c6bc697a99b255928fb8108697 http://data.gdeltproject.org/gdeltv2/20150220070000.mentions.CSV.zip',
     '5391742 236eb6905f33928fadb215a65ed8dd27 http://data.gdeltproject.org/gdeltv2/20150220070000.gkg.csv.zip',
     '96057 7be9c3d5ede640ab4e183591d69afbbe http://data.gdeltproject.org/gdeltv2/20150220071500.export.CSV.zip',
     '180666 7f397447fea408d9f07d3468f4fc5047 http://data.gdeltproject.org/gdeltv2/20150220071500.mentions.CSV.zip',
     '6442632 e5331b91af33bfa1fab522b72ac7f4b7 http://data.gdeltproject.org/gdeltv2/20150220071500.gkg.csv.zip',
     '111807 47d76149121a903432f1a8351c56064e http://data.gdeltproject.org/gdeltv2/20150220073000.export.CSV.zip',
     '180942 53bc0fb62ab9c114884c394668af2132 http://data.gdeltproject.org/gdeltv2/20150220073000.mentions.CSV.zip',
     '6393170 086233dc7f04d5111af70b082f74bc3f http://data.gdeltproject.org/gdeltv2/20150220073000.gkg.csv.zip',
     '112719 1a19946947a06bdd6f2db36753bbd2b9 http://data.gdeltproject.org/gdeltv2/20150220074500.export.CSV.zip',
     '169390 6c117236ccfff3769ed466ebc6d5a90f http://data.gdeltproject.org/gdeltv2/20150220074500.mentions.CSV.zip',
     '5639089 3fc933a6768fe742f797536778874b6d http://data.gdeltproject.org/gdeltv2/20150220074500.gkg.csv.zip',
     '131614 e2754f2ade7e3e30245d3e0e13780f25 http://data.gdeltproject.org/gdeltv2/20150220080000.export.CSV.zip',
     '217762 fed0cedf30720da522261e787494509c http://data.gdeltproject.org/gdeltv2/20150220080000.mentions.CSV.zip',
     '8077096 47032783ac62f293b703f12884f805e1 http://data.gdeltproject.org/gdeltv2/20150220080000.gkg.csv.zip',
     '101402 be49682610943d5cf858e78fafaeadc1 http://data.gdeltproject.org/gdeltv2/20150220081500.export.CSV.zip',
     '173720 18cf68c08474b4e4073f7960ccc470d2 http://data.gdeltproject.org/gdeltv2/20150220081500.mentions.CSV.zip',
     '6416613 d5e528327522af343600b979138952c8 http://data.gdeltproject.org/gdeltv2/20150220081500.gkg.csv.zip',
     '128074 0e7dd9aa232d2cf7ba009c7e3073bbf6 http://data.gdeltproject.org/gdeltv2/20150220083000.export.CSV.zip',
     '208463 2f93ae1e679a1af805391cf8ab1c5097 http://data.gdeltproject.org/gdeltv2/20150220083000.mentions.CSV.zip',
     '7109976 47dfbe4bb1bd4d3c32686de47f054d8f http://data.gdeltproject.org/gdeltv2/20150220083000.gkg.csv.zip',
     '145331 1b0c0ae844aa52d0fe3a7b6446f086b1 http://data.gdeltproject.org/gdeltv2/20150220084500.export.CSV.zip',
     '236790 3e191fcc524c98c5228306562be80db1 http://data.gdeltproject.org/gdeltv2/20150220084500.mentions.CSV.zip',
     '9052286 080dd12c46eedb28a200717b508ebe96 http://data.gdeltproject.org/gdeltv2/20150220084500.gkg.csv.zip',
     '146433 3dd264a09279fb047308ca1f254353c7 http://data.gdeltproject.org/gdeltv2/20150220090000.export.CSV.zip',
     '253712 bbb9d0f49bdacf05c2500fdf50018bba http://data.gdeltproject.org/gdeltv2/20150220090000.mentions.CSV.zip',
     '8943729 8c20f7ac4463a44b3de7a28749be42cd http://data.gdeltproject.org/gdeltv2/20150220090000.gkg.csv.zip',
     '111737 f2813bbc1a8a96df88ce52f629e83c04 http://data.gdeltproject.org/gdeltv2/20150220091500.export.CSV.zip',
     '193751 42ba38f71c2ae60574ec20992f5f8521 http://data.gdeltproject.org/gdeltv2/20150220091500.mentions.CSV.zip',
     '6761130 99efefc6e42b21c5083b7689deaf610b http://data.gdeltproject.org/gdeltv2/20150220091500.gkg.csv.zip',
     '143931 5840be0c7480a3998d9b2e513b409364 http://data.gdeltproject.org/gdeltv2/20150220093000.export.CSV.zip',
     '287132 85b77383b03d739340111051d92cb844 http://data.gdeltproject.org/gdeltv2/20150220093000.mentions.CSV.zip',
     '10640135 32cec750d17b54f80b84830df0e1e41d http://data.gdeltproject.org/gdeltv2/20150220093000.gkg.csv.zip',
     '144803 b252c9fa6839e0dbccb420f768c58549 http://data.gdeltproject.org/gdeltv2/20150220094500.export.CSV.zip',
     '237861 31557239d881b67d4ad0d7c4f5b6e60c http://data.gdeltproject.org/gdeltv2/20150220094500.mentions.CSV.zip',
     '8966217 f160c8f6bc486ae4f12c85868aa4a58e http://data.gdeltproject.org/gdeltv2/20150220094500.gkg.csv.zip',
     '133177 6f8bcdc0d444226cdf57312513411cea http://data.gdeltproject.org/gdeltv2/20150220100000.export.CSV.zip',
     '228152 cd1ded1eafa9e5d442a13e712a209011 http://data.gdeltproject.org/gdeltv2/20150220100000.mentions.CSV.zip',
     '7324836 4e68e00b68527c4d2183bb8c74a08a14 http://data.gdeltproject.org/gdeltv2/20150220100000.gkg.csv.zip',
     '117515 e0e093b1cff27f910975cf5decc144e0 http://data.gdeltproject.org/gdeltv2/20150220101500.export.CSV.zip',
     '229885 2e70a380689002d598651dab2d95f90a http://data.gdeltproject.org/gdeltv2/20150220101500.mentions.CSV.zip',
     '7540766 406b66cd8f5e66766c6943de5e4e4ab9 http://data.gdeltproject.org/gdeltv2/20150220101500.gkg.csv.zip',
     '134243 fc34edd2d3270b28f35832cf578b94f1 http://data.gdeltproject.org/gdeltv2/20150220103000.export.CSV.zip',
     '208516 42814ad78ac1850284b144861ac23e6f http://data.gdeltproject.org/gdeltv2/20150220103000.mentions.CSV.zip',
     '7488417 6372354720e7a0394061bc2c688d6cf2 http://data.gdeltproject.org/gdeltv2/20150220103000.gkg.csv.zip',
     '106727 abaa540ccb321345ffc326a183d3dcf4 http://data.gdeltproject.org/gdeltv2/20150220104500.export.CSV.zip',
     '182929 e3bbc4ef74d1e896e14c0a646d9fef82 http://data.gdeltproject.org/gdeltv2/20150220104500.mentions.CSV.zip',
     '6872892 13037b90bf8cea70229b20de80400fd9 http://data.gdeltproject.org/gdeltv2/20150220104500.gkg.csv.zip',
     '113578 d5d556c17d173514240aaa302890162f http://data.gdeltproject.org/gdeltv2/20150220110000.export.CSV.zip',
     '205713 3f3b51b1172329789fd757e1153344df http://data.gdeltproject.org/gdeltv2/20150220110000.mentions.CSV.zip',
     '7367305 219dcbdd03b1ab209da01cbb28ed19d2 http://data.gdeltproject.org/gdeltv2/20150220110000.gkg.csv.zip',
     '127285 b696627fba40d415c0a6314598f4bc98 http://data.gdeltproject.org/gdeltv2/20150220111500.export.CSV.zip',
     '191314 19b60cc1249ea71fab43e143f4716b63 http://data.gdeltproject.org/gdeltv2/20150220111500.mentions.CSV.zip',
     '6715371 ce325e8f2d753f97964b2ce6a3c0700f http://data.gdeltproject.org/gdeltv2/20150220111500.gkg.csv.zip',
     '107107 e89d502f29dcbc5591721140506eca12 http://data.gdeltproject.org/gdeltv2/20150220113000.export.CSV.zip',
     '176394 550420fc10e21fbddbb4e69360c192cf http://data.gdeltproject.org/gdeltv2/20150220113000.mentions.CSV.zip',
     '7087055 1c41584118c1f8f0f1f5e26a47b0e973 http://data.gdeltproject.org/gdeltv2/20150220113000.gkg.csv.zip',
     '107952 21c154b269218e4566ce2a5ffb9de3e2 http://data.gdeltproject.org/gdeltv2/20150220114500.export.CSV.zip',
     '198157 c3e48d13ae7ac0b6db3365aee0d6e317 http://data.gdeltproject.org/gdeltv2/20150220114500.mentions.CSV.zip',
     '7719609 efd6af401cbc9fd0e01eea551323bb9b http://data.gdeltproject.org/gdeltv2/20150220114500.gkg.csv.zip',
     '94987 93e02f93c0c6f0949eb6b230ce8c3ce0 http://data.gdeltproject.org/gdeltv2/20150220120000.export.CSV.zip',
     '156397 e976d24afc2e8ff2eb8fb6ece172bf3f http://data.gdeltproject.org/gdeltv2/20150220120000.mentions.CSV.zip',
     '6604040 306b9a5ea85ad1c1e23d39f75adbdc24 http://data.gdeltproject.org/gdeltv2/20150220120000.gkg.csv.zip',
     '117391 609b7228c17033e08a3a91c8cc65561a http://data.gdeltproject.org/gdeltv2/20150220121500.export.CSV.zip',
     '187107 773b1dce65ebfb9b98ce81b902ce756a http://data.gdeltproject.org/gdeltv2/20150220121500.mentions.CSV.zip',
     '6365049 0315ef044fe1a3e820b6fee2e8878dd7 http://data.gdeltproject.org/gdeltv2/20150220121500.gkg.csv.zip',
     '142449 e2a09931f6f94596eedb954ba41af441 http://data.gdeltproject.org/gdeltv2/20150220123000.export.CSV.zip',
     '244608 d334380744854441198bbda043a9cca9 http://data.gdeltproject.org/gdeltv2/20150220123000.mentions.CSV.zip',
     '9515711 1dff2f87f4a2bf012eb76e25188308ce http://data.gdeltproject.org/gdeltv2/20150220123000.gkg.csv.zip',
     '154407 4797a6bb565b2df86475dab2bb876a33 http://data.gdeltproject.org/gdeltv2/20150220124500.export.CSV.zip',
     '242700 47d9c1a4eab5cdd2c3b3572847a002ba http://data.gdeltproject.org/gdeltv2/20150220124500.mentions.CSV.zip',
     '8036649 81d01103826e86ba6ebade5f0a8f57f4 http://data.gdeltproject.org/gdeltv2/20150220124500.gkg.csv.zip',
     '101750 fe946138f19c72172a795b5fc1517d2e http://data.gdeltproject.org/gdeltv2/20150220130000.export.CSV.zip',
     '199295 afee6f15a05b62872736bfe4fae99115 http://data.gdeltproject.org/gdeltv2/20150220130000.mentions.CSV.zip',
     '7134196 53538782ab1d49f0880d9a22de35351f http://data.gdeltproject.org/gdeltv2/20150220130000.gkg.csv.zip',
     '129737 d3963465e6f49754a923ab9c5a52543c http://data.gdeltproject.org/gdeltv2/20150220131500.export.CSV.zip',
     '248356 4feae8cc066f60442f28e0770027351d http://data.gdeltproject.org/gdeltv2/20150220131500.mentions.CSV.zip',
     '9857828 4272555fd612ac31511e8198850da2d8 http://data.gdeltproject.org/gdeltv2/20150220131500.gkg.csv.zip',
     '156131 671e4b3bc7343f384e3be5ffcad45d67 http://data.gdeltproject.org/gdeltv2/20150220133000.export.CSV.zip',
     '260449 cb2aa75adaf5caf51482b5e965f8208f http://data.gdeltproject.org/gdeltv2/20150220133000.mentions.CSV.zip',
     '9623181 15a17281a24db741400f3e3f774e03dd http://data.gdeltproject.org/gdeltv2/20150220133000.gkg.csv.zip',
     '165331 1c0de9acc1d4ab26e5b376ed89b3d2a8 http://data.gdeltproject.org/gdeltv2/20150220134500.export.CSV.zip',
     '283783 a0da8c456ba22fc1bb12b271a852e9f3 http://data.gdeltproject.org/gdeltv2/20150220134500.mentions.CSV.zip',
     '10101325 eec42da30ce33778a7654eb2660244cc http://data.gdeltproject.org/gdeltv2/20150220134500.gkg.csv.zip',
     '164496 69ac9b7a63c4e7ed70a2528af747fc5d http://data.gdeltproject.org/gdeltv2/20150220140000.export.CSV.zip',
     '303519 90c99e4e32da7f287d685bc53b57d7a3 http://data.gdeltproject.org/gdeltv2/20150220140000.mentions.CSV.zip',
     '11158963 64ae0604b4ab17374896009fc3b2d493 http://data.gdeltproject.org/gdeltv2/20150220140000.gkg.csv.zip',
     '180444 6badae37a119938072d35458ae623a35 http://data.gdeltproject.org/gdeltv2/20150220141500.export.CSV.zip',
     '303256 c8dd75e26317b5e83cb5d37895cdccfc http://data.gdeltproject.org/gdeltv2/20150220141500.mentions.CSV.zip',
     '10721437 e4fc55dbd4e0a4fedf56d1c895eb404e http://data.gdeltproject.org/gdeltv2/20150220141500.gkg.csv.zip',
     '160374 a05c28af2dc01df416ce8e8bb71c7b75 http://data.gdeltproject.org/gdeltv2/20150220143000.export.CSV.zip',
     '307783 600f161b5962d51021974a494140f3bf http://data.gdeltproject.org/gdeltv2/20150220143000.mentions.CSV.zip',
     '11724579 98a84def104af916661b577f36971d82 http://data.gdeltproject.org/gdeltv2/20150220143000.gkg.csv.zip',
     '165303 b47ac84fccb9ff5da83bf882f7df4a84 http://data.gdeltproject.org/gdeltv2/20150220144500.export.CSV.zip',
     '311033 54dfe0e87ddec1ccc640e2c69e01ee57 http://data.gdeltproject.org/gdeltv2/20150220144500.mentions.CSV.zip',
     '11978537 ccdd5adbe862298c48216bac1c111acb http://data.gdeltproject.org/gdeltv2/20150220144500.gkg.csv.zip',
     '157406 36c66e561d3e17b6448a3d337bcb2335 http://data.gdeltproject.org/gdeltv2/20150220150000.export.CSV.zip',
     '264745 e56a9005322d7c2bc6e6762d6071ec2f http://data.gdeltproject.org/gdeltv2/20150220150000.mentions.CSV.zip',
     '9981744 3d06b33bd32fcd65ef6052c333473042 http://data.gdeltproject.org/gdeltv2/20150220150000.gkg.csv.zip',
     '149971 8aff62f58b2ac72b0c970e92462d4550 http://data.gdeltproject.org/gdeltv2/20150220151500.export.CSV.zip',
     '288400 79da6888495df406bab060a2237dcef0 http://data.gdeltproject.org/gdeltv2/20150220151500.mentions.CSV.zip',
     '10126961 c1c03f4a9a37872143e024dd5b59d063 http://data.gdeltproject.org/gdeltv2/20150220151500.gkg.csv.zip',
     '139742 d3935f17dd81186538014a830bde7d69 http://data.gdeltproject.org/gdeltv2/20150220153000.export.CSV.zip',
     '311479 b24109118ab94b413186544ae2ad196b http://data.gdeltproject.org/gdeltv2/20150220153000.mentions.CSV.zip',
     '10724201 7d606eae88eb24ac4bfdef4a9382e245 http://data.gdeltproject.org/gdeltv2/20150220153000.gkg.csv.zip',
     '161652 9e0b05191bf96fe8438dd3b6e5cc659a http://data.gdeltproject.org/gdeltv2/20150220154500.export.CSV.zip',
     '305577 a6aa48cc4421bd61d6cbdbcc472e7d9e http://data.gdeltproject.org/gdeltv2/20150220154500.mentions.CSV.zip',
     '9881425 1d6639eeaa12f83ac80963cd2875b2f1 http://data.gdeltproject.org/gdeltv2/20150220154500.gkg.csv.zip',
     '152932 c400d24d7ab83dfb4e0f85606bd21d60 http://data.gdeltproject.org/gdeltv2/20150220160000.export.CSV.zip',
     '294930 7949c639944db2defa4c57a32339b311 http://data.gdeltproject.org/gdeltv2/20150220160000.mentions.CSV.zip',
     '9394036 15596797205f9cca853f1474eb5a0781 http://data.gdeltproject.org/gdeltv2/20150220160000.gkg.csv.zip',
     '137369 c468cb3e1b2da9cb225f6139935bb54a http://data.gdeltproject.org/gdeltv2/20150220161500.export.CSV.zip',
     '291243 f418c333f927ecd28cb2398c257972a2 http://data.gdeltproject.org/gdeltv2/20150220161500.mentions.CSV.zip',
     '9874948 40db9f50ec02ab0bf0a529c899c48339 http://data.gdeltproject.org/gdeltv2/20150220161500.gkg.csv.zip',
     '164894 e3bd8b1f9254d1e8eb79f50e52804044 http://data.gdeltproject.org/gdeltv2/20150220163000.export.CSV.zip',
     '298975 ef8819afd3ccfae9528b9b2e7e9bd3ce http://data.gdeltproject.org/gdeltv2/20150220163000.mentions.CSV.zip',
     '10369035 2cd57b8986fb1b80ba2f4aca9f2af242 http://data.gdeltproject.org/gdeltv2/20150220163000.gkg.csv.zip',
     '163706 44ecb4eb485472457204b1538a8a0f8a http://data.gdeltproject.org/gdeltv2/20150220164500.export.CSV.zip',
     '287073 ed092a4f019b6f8c6df85ac91731dcd6 http://data.gdeltproject.org/gdeltv2/20150220164500.mentions.CSV.zip',
     '9718198 0f88e8a474d044ea9690d0bc30bedc1a http://data.gdeltproject.org/gdeltv2/20150220164500.gkg.csv.zip',
     '164363 b06786fd5808a3f4fd714a7d5573b325 http://data.gdeltproject.org/gdeltv2/20150220170000.export.CSV.zip',
     '271713 0c57c321400b9c10850b79e568a6c4a0 http://data.gdeltproject.org/gdeltv2/20150220170000.mentions.CSV.zip',
     '9715079 aa2c485ae3ddc1b8540cf24bd90a5179 http://data.gdeltproject.org/gdeltv2/20150220170000.gkg.csv.zip',
     '162319 2ea1f6f5082dd239e3c4f3a2094b817d http://data.gdeltproject.org/gdeltv2/20150220171500.export.CSV.zip',
     '282920 1e0de9fcada20bba99a6f9aa2fd5d504 http://data.gdeltproject.org/gdeltv2/20150220171500.mentions.CSV.zip',
     '9628711 5f7370dc7b738cc625b5cdfb67471afb http://data.gdeltproject.org/gdeltv2/20150220171500.gkg.csv.zip',
     '163913 49743aa2733508a02a6fc59b31d815dc http://data.gdeltproject.org/gdeltv2/20150220173000.export.CSV.zip',
     '308976 4b43afc0e0e16662fbdd1f229571a30a http://data.gdeltproject.org/gdeltv2/20150220173000.mentions.CSV.zip',
     '10635955 4a7a6c854c8093cae7290523ccec5e7d http://data.gdeltproject.org/gdeltv2/20150220173000.gkg.csv.zip',
     '158980 8d94f4b63995a86dbce4c3a96843da16 http://data.gdeltproject.org/gdeltv2/20150220174500.export.CSV.zip',
     '333932 4189f9704cee13a450f912f2659e51bd http://data.gdeltproject.org/gdeltv2/20150220174500.mentions.CSV.zip',
     '11836124 db4a1e90b2bf371a5a302d88455199c5 http://data.gdeltproject.org/gdeltv2/20150220174500.gkg.csv.zip',
     '153751 4de7e33068024f06ab4b196ed63bb440 http://data.gdeltproject.org/gdeltv2/20150220180000.export.CSV.zip',
     '294645 684be22f114c58d9a8c09753c26e8749 http://data.gdeltproject.org/gdeltv2/20150220180000.mentions.CSV.zip',
     '10020368 01b6c64e1c966bb7452c01ea30d3dc3b http://data.gdeltproject.org/gdeltv2/20150220180000.gkg.csv.zip',
     '171082 14250b3a8aa19ab6c236f250dabee50a http://data.gdeltproject.org/gdeltv2/20150220181500.export.CSV.zip',
     '350731 59af385d85955bc549acd8e50d2a83f0 http://data.gdeltproject.org/gdeltv2/20150220181500.mentions.CSV.zip',
     '11894685 484e0fe16672939c76cd88a942559262 http://data.gdeltproject.org/gdeltv2/20150220181500.gkg.csv.zip',
     '184042 3cdf5e9e46a1697f685a3e324191bba0 http://data.gdeltproject.org/gdeltv2/20150220183000.export.CSV.zip',
     '392681 5511c70a11a0582e6c83ee220dfc68b5 http://data.gdeltproject.org/gdeltv2/20150220183000.mentions.CSV.zip',
     '13144981 e7df5d719deeb65f14762724bdd53c53 http://data.gdeltproject.org/gdeltv2/20150220183000.gkg.csv.zip',
     '178108 60e9659e79182c01e73bbff60d17283a http://data.gdeltproject.org/gdeltv2/20150220184500.export.CSV.zip',
     '370430 1aeb28bafa39aa75808bd437e59ee92d http://data.gdeltproject.org/gdeltv2/20150220184500.mentions.CSV.zip',
     '12486723 7098cb3b065d2aa948bf9e42e2e8ce97 http://data.gdeltproject.org/gdeltv2/20150220184500.gkg.csv.zip',
     '162584 effb1f1661c73290aa8de8b9df080806 http://data.gdeltproject.org/gdeltv2/20150220190000.export.CSV.zip',
     '324424 22f435b262c1af8b4d73c4705d15256d http://data.gdeltproject.org/gdeltv2/20150220190000.mentions.CSV.zip',
     '11637196 ff34c4d4c3ff0e7b59387a69b9860b53 http://data.gdeltproject.org/gdeltv2/20150220190000.gkg.csv.zip',
     '181057 2fc5897adb87c6119e763b11cca5a637 http://data.gdeltproject.org/gdeltv2/20150220191500.export.CSV.zip',
     '344372 4e82e834f5e6c819e7bf085d24e8af59 http://data.gdeltproject.org/gdeltv2/20150220191500.mentions.CSV.zip',
     '12111440 911ed919eb37043f5fc8a87146502249 http://data.gdeltproject.org/gdeltv2/20150220191500.gkg.csv.zip',
     '175027 fe2d2f573f1ed1f150d5f7477192fed7 http://data.gdeltproject.org/gdeltv2/20150220193000.export.CSV.zip',
     '341509 1d0349676e627fd3e96247d52ee8adac http://data.gdeltproject.org/gdeltv2/20150220193000.mentions.CSV.zip',
     '11422612 114a0531d526bd126905a2d8ead44787 http://data.gdeltproject.org/gdeltv2/20150220193000.gkg.csv.zip',
     '158765 d139d77a0bce6f02f661e680929e5978 http://data.gdeltproject.org/gdeltv2/20150220194500.export.CSV.zip',
     '306595 7c2b2a5774c5008b7c364bfcc969539a http://data.gdeltproject.org/gdeltv2/20150220194500.mentions.CSV.zip',
     '10136804 9b332d2d285a3ac84d0c025b3194fcdd http://data.gdeltproject.org/gdeltv2/20150220194500.gkg.csv.zip',
     '120325 aead8f04c3b44bad2080f6dc3679e9b1 http://data.gdeltproject.org/gdeltv2/20150220200000.export.CSV.zip',
     '289794 9b4ae6bf8538e21c426f70ec9293e9aa http://data.gdeltproject.org/gdeltv2/20150220200000.mentions.CSV.zip',
     '10120369 0b750455d66f1dcd5b61fce2977f06ce http://data.gdeltproject.org/gdeltv2/20150220200000.gkg.csv.zip',
     '150621 7db349933c5ae545569c52d363531537 http://data.gdeltproject.org/gdeltv2/20150220201500.export.CSV.zip',
     '284363 bb0507b03bb916c5cf6d74c2997bc46d http://data.gdeltproject.org/gdeltv2/20150220201500.mentions.CSV.zip',
     '9731803 db358dd6b3dd2e0bfd412b43f8213a8e http://data.gdeltproject.org/gdeltv2/20150220201500.gkg.csv.zip',
     '144964 a03713912263e6b28be1b393a840c8ec http://data.gdeltproject.org/gdeltv2/20150220203000.export.CSV.zip',
     '251702 c57f5fae7306bf14a9a596cf669a13bb http://data.gdeltproject.org/gdeltv2/20150220203000.mentions.CSV.zip',
     '8527195 fc5c7f00f78b03f4759e6b71538e806d http://data.gdeltproject.org/gdeltv2/20150220203000.gkg.csv.zip',
     '134626 53cbb16c167d460381b93ea83cc5cf38 http://data.gdeltproject.org/gdeltv2/20150220204500.export.CSV.zip',
     '284662 ca9ae6d860d9e95330c67bb786936d38 http://data.gdeltproject.org/gdeltv2/20150220204500.mentions.CSV.zip',
     '9736592 637ebff410801fa3f0ec43950584543b http://data.gdeltproject.org/gdeltv2/20150220204500.gkg.csv.zip',
     '136966 95f3fbd5f7ea20c9c0ad828861e7d5f5 http://data.gdeltproject.org/gdeltv2/20150220210000.export.CSV.zip',
     '284615 975f6647af3708de214767a2c8856b3b http://data.gdeltproject.org/gdeltv2/20150220210000.mentions.CSV.zip',
     '9336550 d484b216ded24776c8dfe8e8e0f096df http://data.gdeltproject.org/gdeltv2/20150220210000.gkg.csv.zip',
     '125700 d0fe09b51c04c99a08fca5da0e708991 http://data.gdeltproject.org/gdeltv2/20150220211500.export.CSV.zip',
     '247030 f0aa18df408051572094ff5427410119 http://data.gdeltproject.org/gdeltv2/20150220211500.mentions.CSV.zip',
     '8278132 c4f40065aaaf105dcc3bcb8d14edcd6a http://data.gdeltproject.org/gdeltv2/20150220211500.gkg.csv.zip',
     '133771 5b9055e8c060fa54af954f577a9cf58c http://data.gdeltproject.org/gdeltv2/20150220213000.export.CSV.zip',
     '278067 8d8a69b8cfaeeff452c4cddb0239552d http://data.gdeltproject.org/gdeltv2/20150220213000.mentions.CSV.zip',
     '9730211 0896606b9dd2c3773d1fccf83e4b2e68 http://data.gdeltproject.org/gdeltv2/20150220213000.gkg.csv.zip',
     '141085 89cabb4ac0a04503dd6944291f276bbb http://data.gdeltproject.org/gdeltv2/20150220214500.export.CSV.zip',
     '282757 7e5310f0c66a176280d1f7a7b2d0e3d8 http://data.gdeltproject.org/gdeltv2/20150220214500.mentions.CSV.zip',
     '8362677 059693c45bcf796fed87a03b7bf8398b http://data.gdeltproject.org/gdeltv2/20150220214500.gkg.csv.zip',
     '115952 5529fc375bbf2b226425dc789d93e827 http://data.gdeltproject.org/gdeltv2/20150220220000.export.CSV.zip',
     '253327 7a8ae8de78835665bc7cd7208ebb3504 http://data.gdeltproject.org/gdeltv2/20150220220000.mentions.CSV.zip',
     '8702415 9e3dbb1df76b94e0994b22898f758cb5 http://data.gdeltproject.org/gdeltv2/20150220220000.gkg.csv.zip',
     '124149 92b04161f27139324fd077d5cc9298d6 http://data.gdeltproject.org/gdeltv2/20150220221500.export.CSV.zip',
     '285835 001b07284b5ed6e1769902d7eb6d08ef http://data.gdeltproject.org/gdeltv2/20150220221500.mentions.CSV.zip',
     '9788448 8eba079fcabba92680b37907d55c840d http://data.gdeltproject.org/gdeltv2/20150220221500.gkg.csv.zip',
     '138585 9e113836cb47c9c40a36d90722255b95 http://data.gdeltproject.org/gdeltv2/20150220223000.export.CSV.zip',
     '308112 9a412f0b6430d2ba01c9aea48d0ee703 http://data.gdeltproject.org/gdeltv2/20150220223000.mentions.CSV.zip',
     '10348473 1a25b415e97f594079b583150c4f2c1f http://data.gdeltproject.org/gdeltv2/20150220223000.gkg.csv.zip',
     '113930 2b41048b1bf5e7259988703a5d72fcad http://data.gdeltproject.org/gdeltv2/20150220224500.export.CSV.zip',
     '274751 d469411af18e4882ca3f6409fd4295a8 http://data.gdeltproject.org/gdeltv2/20150220224500.mentions.CSV.zip',
     '8476547 1cdead9a9e732a8b7296aa23554a3dc3 http://data.gdeltproject.org/gdeltv2/20150220224500.gkg.csv.zip',
     '135157 6e5e777f9a2ddc96c589189b4868e29b http://data.gdeltproject.org/gdeltv2/20150220230000.export.CSV.zip',
     '297219 83d28b1397a1690dd142f0cc3294a454 http://data.gdeltproject.org/gdeltv2/20150220230000.mentions.CSV.zip',
     '9896403 44dded71b830395362bd5da4f4fecfa4 http://data.gdeltproject.org/gdeltv2/20150220230000.gkg.csv.zip',
     '24355 5c51e0675d5946b3ea8c3cc844b3c22f http://data.gdeltproject.org/gdeltv2/20150220231500.export.CSV.zip',
     '53948 df9a9c2ecdeafb7d004bd90065fb955f http://data.gdeltproject.org/gdeltv2/20150220231500.mentions.CSV.zip',
     '9734111 9a5aeaa84f278b04239f44a94317a35f http://data.gdeltproject.org/gdeltv2/20150220231500.gkg.csv.zip',
     '140304 984eacadcf34ec021b975c8740001200 http://data.gdeltproject.org/gdeltv2/20150220233000.export.CSV.zip',
     '259582 e24c3c4c7113a2cd898f6ecc5639cc8c http://data.gdeltproject.org/gdeltv2/20150220233000.mentions.CSV.zip',
     '9336861 2057fdc5ce2ecea03f6d059f1b11c71d http://data.gdeltproject.org/gdeltv2/20150220233000.gkg.csv.zip',
     '157001 c853359c48c9e4cc3c0ee0b31b578fa9 http://data.gdeltproject.org/gdeltv2/20150220234500.export.CSV.zip',
     '344058 ce39547f3513e63c352a224a9033824f http://data.gdeltproject.org/gdeltv2/20150220234500.mentions.CSV.zip',
     '11379901 9fc6e50ef867caed3ac8202cd1c76986 http://data.gdeltproject.org/gdeltv2/20150220234500.gkg.csv.zip',
     '316836 e9190d33f696334c1c95d65f15bffb93 http://data.gdeltproject.org/gdeltv2/20150221000000.export.CSV.zip',
     '250907 3b89d6cd317c555c4b976d5d79fe47cb http://data.gdeltproject.org/gdeltv2/20150221000000.mentions.CSV.zip',
     '9421746 78191e4f7e21cbb911b018e269538c7e http://data.gdeltproject.org/gdeltv2/20150221000000.gkg.csv.zip',
     '218302 c477f526bc1cf199f1ebedea307df967 http://data.gdeltproject.org/gdeltv2/20150221001500.export.CSV.zip',
     '208662 164b981f655943b7d2ed5bf524f4da10 http://data.gdeltproject.org/gdeltv2/20150221001500.mentions.CSV.zip',
     '8228105 802fbfa2a5b6a1074c82b10c7941d6ee http://data.gdeltproject.org/gdeltv2/20150221001500.gkg.csv.zip',
     '250110 4d71bc6ab51a440eb9d89df5caaddb48 http://data.gdeltproject.org/gdeltv2/20150221003000.export.CSV.zip',
     '276876 9cf27d5770c7ff8a637d52557a9ce538 http://data.gdeltproject.org/gdeltv2/20150221003000.mentions.CSV.zip',
     '9515144 8497626083d6fdddf11d4172699e2643 http://data.gdeltproject.org/gdeltv2/20150221003000.gkg.csv.zip',
     '163934 1e3c1ae78262eb92f9482f5fc3c8feca http://data.gdeltproject.org/gdeltv2/20150221004500.export.CSV.zip',
     '200307 908d07b1ab74d9dc934416b09c77a96a http://data.gdeltproject.org/gdeltv2/20150221004500.mentions.CSV.zip',
     '7727696 7579145cce1f3fb5daab89dc50edadf2 http://data.gdeltproject.org/gdeltv2/20150221004500.gkg.csv.zip',
     '160325 70652806990d72af8a25c59ab0194b1e http://data.gdeltproject.org/gdeltv2/20150221010000.export.CSV.zip',
     '184839 097781a2dfb9d56c6c931fd29cb3588f http://data.gdeltproject.org/gdeltv2/20150221010000.mentions.CSV.zip',
     '6911712 63b8eccb2e0dd15c09088eec8c47f8cd http://data.gdeltproject.org/gdeltv2/20150221010000.gkg.csv.zip',
     '187424 2c55c69ad9ca883c95140cf063d96407 http://data.gdeltproject.org/gdeltv2/20150221011500.export.CSV.zip',
     '236650 b0fb87964eb74a847afff1681a7fec9c http://data.gdeltproject.org/gdeltv2/20150221011500.mentions.CSV.zip',
     '8024834 78ad95aab96a31f7757334b5620a894d http://data.gdeltproject.org/gdeltv2/20150221011500.gkg.csv.zip',
     '138093 ed3d5aadfb1c3ba92b859ba23ed73ecf http://data.gdeltproject.org/gdeltv2/20150221013000.export.CSV.zip',
     '176915 182cfcd28fbe84e7863c31ea016b85dc http://data.gdeltproject.org/gdeltv2/20150221013000.mentions.CSV.zip',
     '6295978 7f131bdc1a70449af2847f68904203a6 http://data.gdeltproject.org/gdeltv2/20150221013000.gkg.csv.zip',
     '112673 e08b08fc413cc0982067d82dbf2ff2eb http://data.gdeltproject.org/gdeltv2/20150221014500.export.CSV.zip',
     '151604 a087fa787d90619ab877676e800696c2 http://data.gdeltproject.org/gdeltv2/20150221014500.mentions.CSV.zip',
     '5469532 6daca5977842e8ade9fe699e2dc4858b http://data.gdeltproject.org/gdeltv2/20150221014500.gkg.csv.zip',
     '123853 74ec0bb7fac390680eca597840de8d8c http://data.gdeltproject.org/gdeltv2/20150221021500.export.CSV.zip',
     '164511 e1c6f29736b676db2ea57ab76f050d0c http://data.gdeltproject.org/gdeltv2/20150221021500.mentions.CSV.zip',
     '5350802 bd270c6f314096cd82b31f027e6b81a4 http://data.gdeltproject.org/gdeltv2/20150221021500.gkg.csv.zip',
     '111511 69272917e7d76a4244939dcff46cc25c http://data.gdeltproject.org/gdeltv2/20150221020000.export.CSV.zip',
     '158097 3ffedca8a473662270a36ff028e2b5db http://data.gdeltproject.org/gdeltv2/20150221020000.mentions.CSV.zip',
     '5670579 154d55a85c033fa72e1dada4333e03cf http://data.gdeltproject.org/gdeltv2/20150221020000.gkg.csv.zip',
     '87240 82b2f31919ad8c330b38c104f261563f http://data.gdeltproject.org/gdeltv2/20150221023000.export.CSV.zip',
     '127208 aefdf299164327bd662c3eafa8229a33 http://data.gdeltproject.org/gdeltv2/20150221023000.mentions.CSV.zip',
     '4594685 2950b6a7be03acecec0bcc04f2cd3f90 http://data.gdeltproject.org/gdeltv2/20150221023000.gkg.csv.zip',
     '140645 678e08c815792747bca0c956f2f38aa4 http://data.gdeltproject.org/gdeltv2/20150221024500.export.CSV.zip',
     '181864 c41b8435060492e08ce16cafc4081baa http://data.gdeltproject.org/gdeltv2/20150221024500.mentions.CSV.zip',
     '6493841 d47958a4b9d93471faaf5c01d32a1efe http://data.gdeltproject.org/gdeltv2/20150221024500.gkg.csv.zip',
     '101662 4a7002bdb40a0e8af63dc6467f104a02 http://data.gdeltproject.org/gdeltv2/20150221030000.export.CSV.zip',
     '153400 b92aaa8ee801a4e31b833dae69d57053 http://data.gdeltproject.org/gdeltv2/20150221030000.mentions.CSV.zip',
     '5369284 3dc44b27c856ba90b86bc886a91cabbd http://data.gdeltproject.org/gdeltv2/20150221030000.gkg.csv.zip',
     '105576 d46c34c31d0c2b17a2ac728b41c7a57c http://data.gdeltproject.org/gdeltv2/20150221031500.export.CSV.zip',
     '156429 d560a569abf4d7a4ef7eb41886d4470c http://data.gdeltproject.org/gdeltv2/20150221031500.mentions.CSV.zip',
     '5719894 8bf9f5858c789422877d0b6725575288 http://data.gdeltproject.org/gdeltv2/20150221031500.gkg.csv.zip',
     '121097 a7fe03ae60f0a1e9e66560b264f6c873 http://data.gdeltproject.org/gdeltv2/20150221033000.export.CSV.zip',
     '189873 7ed4cfc5faa79b4018155e156d6c407e http://data.gdeltproject.org/gdeltv2/20150221033000.mentions.CSV.zip',
     '6787771 4912c6255efc243bcb26169c871981b0 http://data.gdeltproject.org/gdeltv2/20150221033000.gkg.csv.zip',
     '122081 298869056a487960c6ad6c459dd62bcc http://data.gdeltproject.org/gdeltv2/20150221034500.export.CSV.zip',
     '157464 175de684e1b05fcf0c2dc28c1e413741 http://data.gdeltproject.org/gdeltv2/20150221034500.mentions.CSV.zip',
     '5676475 67ed12df47815a42ee81cdc7b670dff4 http://data.gdeltproject.org/gdeltv2/20150221034500.gkg.csv.zip',
     '145471 33c83006f0433fb4a2a5ec80fbd8da92 http://data.gdeltproject.org/gdeltv2/20150221040000.export.CSV.zip',
     '196268 a3aca4cbbd2c7d50e91f9c133764ee84 http://data.gdeltproject.org/gdeltv2/20150221040000.mentions.CSV.zip',
     '6332683 ebc73441d829375dac47d6f76abbfd73 http://data.gdeltproject.org/gdeltv2/20150221040000.gkg.csv.zip',
     '109596 9ac06dcb61da7647076fc8e96f3d9b76 http://data.gdeltproject.org/gdeltv2/20150221041500.export.CSV.zip',
     '192109 34c55ad8a91f68abeada48b2dd350db1 http://data.gdeltproject.org/gdeltv2/20150221041500.mentions.CSV.zip',
     '6638844 6a7969bd80b4ac13a7f22612da1fcd7e http://data.gdeltproject.org/gdeltv2/20150221041500.gkg.csv.zip',
     '93567 73ebc42bfcd6291c4833c0d893049615 http://data.gdeltproject.org/gdeltv2/20150221043000.export.CSV.zip',
     '159170 02b17b6608e6e4a181657ea6dfbb7e00 http://data.gdeltproject.org/gdeltv2/20150221043000.mentions.CSV.zip',
     '6040373 6274b1344320e7f6a18e5590de6da7dc http://data.gdeltproject.org/gdeltv2/20150221043000.gkg.csv.zip',
     '95103 6e0da2ad34dbe2511118447a55a9c98f http://data.gdeltproject.org/gdeltv2/20150221044500.export.CSV.zip',
     '157771 11cd218b9cb97dd02026c293b36865c5 http://data.gdeltproject.org/gdeltv2/20150221044500.mentions.CSV.zip',
     '5484608 0fe2ee7eb56a871a8e4e9abbaf0da2d2 http://data.gdeltproject.org/gdeltv2/20150221044500.gkg.csv.zip',
     '98011 b31c2262072ea516b2b5ac415d647440 http://data.gdeltproject.org/gdeltv2/20150221050000.export.CSV.zip',
     '151432 3bfb38e0733523fa6cf156e658c5cc8a http://data.gdeltproject.org/gdeltv2/20150221050000.mentions.CSV.zip',
     '5188569 dd00b9e7a8575575b455e6be100bae8d http://data.gdeltproject.org/gdeltv2/20150221050000.gkg.csv.zip',
     '75407 01de7f40cf048419be9a08feffbc0400 http://data.gdeltproject.org/gdeltv2/20150221051500.export.CSV.zip',
     '127700 4f336ee78822d03de8ab7469ff532aad http://data.gdeltproject.org/gdeltv2/20150221051500.mentions.CSV.zip',
     '5034754 4b0599e2f248cee8606490702515697f http://data.gdeltproject.org/gdeltv2/20150221051500.gkg.csv.zip',
     '100889 c02db3c13cf894687544a49931f8fb41 http://data.gdeltproject.org/gdeltv2/20150221053000.export.CSV.zip',
     '169494 564fcfcac892a3daaadd8fc8c1f628bc http://data.gdeltproject.org/gdeltv2/20150221053000.mentions.CSV.zip',
     '5764455 02d56df763d2cb302147b2b3e48426b3 http://data.gdeltproject.org/gdeltv2/20150221053000.gkg.csv.zip',
     '96032 1273038bcab16302e8ebe5c88bef8377 http://data.gdeltproject.org/gdeltv2/20150221054500.export.CSV.zip',
     '173106 9c44aca7d161ebed172c785afd86cbd5 http://data.gdeltproject.org/gdeltv2/20150221054500.mentions.CSV.zip',
     '5919066 71200be061043769f4ae4b3a43d7ee52 http://data.gdeltproject.org/gdeltv2/20150221054500.gkg.csv.zip',
     '68292 371d5df59b5f6d9011e00a858f31dcf7 http://data.gdeltproject.org/gdeltv2/20150221060000.export.CSV.zip',
     '131205 4f4f0165bac1c639e6eef8269897c406 http://data.gdeltproject.org/gdeltv2/20150221060000.mentions.CSV.zip',
     '4611612 769f5276017d5d8a7ba11d38bbe19afe http://data.gdeltproject.org/gdeltv2/20150221060000.gkg.csv.zip',
     '60419 7b74ba12062cdeda970ff4c78a93a050 http://data.gdeltproject.org/gdeltv2/20150221061500.export.CSV.zip',
     '108444 e10a0fcac700276d14b56a03591d4c70 http://data.gdeltproject.org/gdeltv2/20150221061500.mentions.CSV.zip',
     '4831916 4bee1e9eb19c85a0c2d5f23a9a631f04 http://data.gdeltproject.org/gdeltv2/20150221061500.gkg.csv.zip',
     '98667 c68698ba752126a57fb99f653cffb90e http://data.gdeltproject.org/gdeltv2/20150221063000.export.CSV.zip',
     '148093 7a5883810848f2e0258cdda83cd48d9f http://data.gdeltproject.org/gdeltv2/20150221063000.mentions.CSV.zip',
     '5736788 f695a6c33d5d8e6e11fe3b8b4c737971 http://data.gdeltproject.org/gdeltv2/20150221063000.gkg.csv.zip',
     '98788 515ef30407ad4483a5469f354d7cc473 http://data.gdeltproject.org/gdeltv2/20150221064500.export.CSV.zip',
     '144140 f27c95e7401a74ba750b33e868c9ac61 http://data.gdeltproject.org/gdeltv2/20150221064500.mentions.CSV.zip',
     '5496537 2a36f451b14e008b9581e5c8e9dd8bbe http://data.gdeltproject.org/gdeltv2/20150221064500.gkg.csv.zip',
     '64099 108a472ddcd2e304c0473346c2fbf807 http://data.gdeltproject.org/gdeltv2/20150221070000.export.CSV.zip',
     '123345 6d74a8f665aa2bce82a72a0d2c21d4dc http://data.gdeltproject.org/gdeltv2/20150221070000.mentions.CSV.zip',
     '5168448 e27052fb2cd22cab354bc6c8121cd464 http://data.gdeltproject.org/gdeltv2/20150221070000.gkg.csv.zip',
     '70655 efaa5ede092f5e22a53582dd75e26726 http://data.gdeltproject.org/gdeltv2/20150221071500.export.CSV.zip',
     '121398 41719e682f3dabf5059f3187bac52abc http://data.gdeltproject.org/gdeltv2/20150221071500.mentions.CSV.zip',
     '4945042 f2867d40a89ba211d5faf7c301c337bf http://data.gdeltproject.org/gdeltv2/20150221071500.gkg.csv.zip',
     '68720 2519b1baf2368669edba69598d415ecd http://data.gdeltproject.org/gdeltv2/20150221073000.export.CSV.zip',
     '128757 2234b4469f500f34205f64e6f9c55357 http://data.gdeltproject.org/gdeltv2/20150221073000.mentions.CSV.zip',
     '4706859 f3a3ed3b1942bf38d431ab4da3b021ef http://data.gdeltproject.org/gdeltv2/20150221073000.gkg.csv.zip',
     '57426 cbe255f8c0e2fc36cc9d87bb2d95a0eb http://data.gdeltproject.org/gdeltv2/20150221074500.export.CSV.zip',
     '99045 a7830c97ce51ecfa62523c86a2a077dd http://data.gdeltproject.org/gdeltv2/20150221074500.mentions.CSV.zip',
     '3972798 b5cff99c9ec4875ae96fa7405dd7dbe2 http://data.gdeltproject.org/gdeltv2/20150221074500.gkg.csv.zip',
     '78257 9740714d1bcef8185e972f479453c0a2 http://data.gdeltproject.org/gdeltv2/20150221080000.export.CSV.zip',
     '131968 e310b62c132a0ea0748a0cd8cd87457c http://data.gdeltproject.org/gdeltv2/20150221080000.mentions.CSV.zip',
     '5646824 8146887ec76621e79546e96f7325dd19 http://data.gdeltproject.org/gdeltv2/20150221080000.gkg.csv.zip',
     '67793 b49832be50f4dc7171b869dcfa1afd54 http://data.gdeltproject.org/gdeltv2/20150221081500.export.CSV.zip',
     '114211 229dabc02be7b29c67a9e273d62bffce http://data.gdeltproject.org/gdeltv2/20150221081500.mentions.CSV.zip',
     '4341100 b9e8185195e4abfc5c011dc769db9f17 http://data.gdeltproject.org/gdeltv2/20150221081500.gkg.csv.zip',
     '92070 c9224473fa180fc2a59066a7b04ada31 http://data.gdeltproject.org/gdeltv2/20150221083000.export.CSV.zip',
     '157942 49134750943c58556d30b14c38717685 http://data.gdeltproject.org/gdeltv2/20150221083000.mentions.CSV.zip',
     '5570214 b2e9a17c901358e43116e8aeb0c4abfb http://data.gdeltproject.org/gdeltv2/20150221083000.gkg.csv.zip',
     '82336 aadee1fa641ba637ae1e336c152a3031 http://data.gdeltproject.org/gdeltv2/20150221084500.export.CSV.zip',
     '131938 8ff2f3c858599939e88358586fc2869a http://data.gdeltproject.org/gdeltv2/20150221084500.mentions.CSV.zip',
     '5274839 88550a582d7e16272d99f023d88e6ed4 http://data.gdeltproject.org/gdeltv2/20150221084500.gkg.csv.zip',
     '66711 4149b034b749f972a8001d4eacc81d8f http://data.gdeltproject.org/gdeltv2/20150221090000.export.CSV.zip',
     '133248 e99d6fdd78f27ec4d03bd6979b53d1dd http://data.gdeltproject.org/gdeltv2/20150221090000.mentions.CSV.zip',
     '4560833 9e202ee36531f41eb9cebba0670f2763 http://data.gdeltproject.org/gdeltv2/20150221090000.gkg.csv.zip',
     '73173 1931d18736de815a4f14d4f228f7f846 http://data.gdeltproject.org/gdeltv2/20150221091500.export.CSV.zip',
     '138313 dc9c371409ac79534ff4a5895ed65e53 http://data.gdeltproject.org/gdeltv2/20150221091500.mentions.CSV.zip',
     '5207687 cb55f69571ecd0b8765411a39dcb0b6f http://data.gdeltproject.org/gdeltv2/20150221091500.gkg.csv.zip',
     '93430 c05b8f86204b97a8f08fb6778ec229e5 http://data.gdeltproject.org/gdeltv2/20150221093000.export.CSV.zip',
     '178561 c7deaad19b2450a4040c10e41a2ff359 http://data.gdeltproject.org/gdeltv2/20150221093000.mentions.CSV.zip',
     '6547352 1d8927800edaece9171bfa59e6144e09 http://data.gdeltproject.org/gdeltv2/20150221093000.gkg.csv.zip',
     '77493 938b4693e6d81bbaf394e5ef3741255d http://data.gdeltproject.org/gdeltv2/20150221094500.export.CSV.zip',
     '141652 0434812ad0d9fbeb66e911d61aac378c http://data.gdeltproject.org/gdeltv2/20150221094500.mentions.CSV.zip',
     '5280756 c1f296c695eaaa5436fe968095943768 http://data.gdeltproject.org/gdeltv2/20150221094500.gkg.csv.zip',
     '74192 3a4e3cd2b521ccff4f104454974558e9 http://data.gdeltproject.org/gdeltv2/20150221100000.export.CSV.zip',
     '139161 fa9fae6e8f44aa7926dda42aa6f5adc9 http://data.gdeltproject.org/gdeltv2/20150221100000.mentions.CSV.zip',
     '4446864 216f5bfd25287111c9cb08b2cb8f6276 http://data.gdeltproject.org/gdeltv2/20150221100000.gkg.csv.zip',
     '50595 5048a37f07b37e9350b77226b6fc22ba http://data.gdeltproject.org/gdeltv2/20150221101500.export.CSV.zip',
     '154348 e0719137cc55eca37b20d2980b3e4a19 http://data.gdeltproject.org/gdeltv2/20150221101500.mentions.CSV.zip',
     '4818940 d99654953d1f7c80aac696f20c22510c http://data.gdeltproject.org/gdeltv2/20150221101500.gkg.csv.zip',
     '82819 71b38f093fbcf5dfa207c9d56f94bf90 http://data.gdeltproject.org/gdeltv2/20150221103000.export.CSV.zip',
     '158408 0bf0b5248d29c5621fab634665dc4848 http://data.gdeltproject.org/gdeltv2/20150221103000.mentions.CSV.zip',
     '5038098 2e9e8f954ab29b6544e06fd94d23ebf8 http://data.gdeltproject.org/gdeltv2/20150221103000.gkg.csv.zip',
     '69934 6f29ce2b8e9602819bf7d14c27e727f8 http://data.gdeltproject.org/gdeltv2/20150221104500.export.CSV.zip',
     '136064 a2a0b5700843d3e983088a7530aa8188 http://data.gdeltproject.org/gdeltv2/20150221104500.mentions.CSV.zip',
     '4292906 fab5d7bb029324195d66bf84bdd38f47 http://data.gdeltproject.org/gdeltv2/20150221104500.gkg.csv.zip',
     '64662 79295d9ba10e0b422622c91a864785b7 http://data.gdeltproject.org/gdeltv2/20150221110000.export.CSV.zip',
     '148417 df946ff483a773f94c9d50113066c3b7 http://data.gdeltproject.org/gdeltv2/20150221110000.mentions.CSV.zip',
     '4821902 7afbf2d418c2f8e37e295be15f1c0253 http://data.gdeltproject.org/gdeltv2/20150221110000.gkg.csv.zip',
     '67254 8e1d17cf5938464651c7b5088a2ad5e6 http://data.gdeltproject.org/gdeltv2/20150221111500.export.CSV.zip',
     '128667 3e2ba484cb4fe34119e33b10bdcb453a http://data.gdeltproject.org/gdeltv2/20150221111500.mentions.CSV.zip',
     '4295766 f1438816845ac92f2a4203744668f14b http://data.gdeltproject.org/gdeltv2/20150221111500.gkg.csv.zip',
     '63628 7dddfe6d1b7db0dd9dda2408d6db5778 http://data.gdeltproject.org/gdeltv2/20150221113000.export.CSV.zip',
     '106487 29a186aa5b27f01cae1586f433288b8c http://data.gdeltproject.org/gdeltv2/20150221113000.mentions.CSV.zip',
     '3652779 c64c06ed5f6a89c2406c0f20c23bc350 http://data.gdeltproject.org/gdeltv2/20150221113000.gkg.csv.zip',
     '75210 57b5eb6c9c78fbb6a712df12dab7aa9c http://data.gdeltproject.org/gdeltv2/20150221114500.export.CSV.zip',
     '141628 7c399cdac455eafcd200ca9952da7081 http://data.gdeltproject.org/gdeltv2/20150221114500.mentions.CSV.zip',
     '4423652 e5dc47961c182a1f07d8b7d0ae0b730e http://data.gdeltproject.org/gdeltv2/20150221114500.gkg.csv.zip',
     '63656 8cfebd35c936bcffece831e108514ccc http://data.gdeltproject.org/gdeltv2/20150221120000.export.CSV.zip',
     '144973 21801b55f62e226b940789a79f0f34fd http://data.gdeltproject.org/gdeltv2/20150221120000.mentions.CSV.zip',
     '4504693 1ab75f444b47ce8fbd9dddd1e4dd1ca2 http://data.gdeltproject.org/gdeltv2/20150221120000.gkg.csv.zip',
     '58097 c0e8e3f2614373b798c89c0483796460 http://data.gdeltproject.org/gdeltv2/20150221121500.export.CSV.zip',
     '121045 daec61cf3d1f4e87e77c97a0513fbae6 http://data.gdeltproject.org/gdeltv2/20150221121500.mentions.CSV.zip',
     '3486870 7574638f519607ac1af00cdb63002dc0 http://data.gdeltproject.org/gdeltv2/20150221121500.gkg.csv.zip',
     '76483 56b06a983893cc8216d9e023c3eaa98e http://data.gdeltproject.org/gdeltv2/20150221123000.export.CSV.zip',
     '160197 0e4cd5e0855f1d24f97b548cc9723bf0 http://data.gdeltproject.org/gdeltv2/20150221123000.mentions.CSV.zip',
     '4634782 729cb58f37c23240ff5f38d113fe2e78 http://data.gdeltproject.org/gdeltv2/20150221123000.gkg.csv.zip',
     '88922 9e6694bb6c2c2ea3b1766ffec6fe67e2 http://data.gdeltproject.org/gdeltv2/20150221124500.export.CSV.zip',
     '175422 9993d06b2d0dcebb2a0f7b8c3ed0e6d9 http://data.gdeltproject.org/gdeltv2/20150221124500.mentions.CSV.zip',
     '4977723 1af9cd3fe21431266ae94c6fd75ccee3 http://data.gdeltproject.org/gdeltv2/20150221124500.gkg.csv.zip',
     '77707 74d2388fac88d4f061b3f1960656632e http://data.gdeltproject.org/gdeltv2/20150221130000.export.CSV.zip',
     '159067 780328a8d167fcff387075eb978c9353 http://data.gdeltproject.org/gdeltv2/20150221130000.mentions.CSV.zip',
     '4709822 37ff97973d8ada4b3cfa82772b65ac0d http://data.gdeltproject.org/gdeltv2/20150221130000.gkg.csv.zip',
     '84489 af89a474936d9478452e756e033fd8f5 http://data.gdeltproject.org/gdeltv2/20150221131500.export.CSV.zip',
     '176448 1f80006a367d6f7e2c7d16e0e5d8841d http://data.gdeltproject.org/gdeltv2/20150221131500.mentions.CSV.zip',
     '5123013 6736556d279587e8f3e0d0cf7fb929f5 http://data.gdeltproject.org/gdeltv2/20150221131500.gkg.csv.zip',
     '108914 b2f40ee473f80eacedb96f27c6f47fe9 http://data.gdeltproject.org/gdeltv2/20150221133000.export.CSV.zip',
     '199472 85ff9142ce538bb86e3d4f269187a29a http://data.gdeltproject.org/gdeltv2/20150221133000.mentions.CSV.zip',
     '5549568 c75d2e3a062d05aeac461ddff9e420fd http://data.gdeltproject.org/gdeltv2/20150221133000.gkg.csv.zip',
     '93701 ec8f50e8975362e2f0a3aae3f94313db http://data.gdeltproject.org/gdeltv2/20150221134500.export.CSV.zip',
     '210580 dc6bf43c5179875e3bb8dd0a0bdd59f1 http://data.gdeltproject.org/gdeltv2/20150221134500.mentions.CSV.zip',
     '5961948 0ebf7046c0e43e0c353c1ee5233d134f http://data.gdeltproject.org/gdeltv2/20150221134500.gkg.csv.zip',
     '112985 284589d133ad3b702ee9516dad1b0ce9 http://data.gdeltproject.org/gdeltv2/20150221140000.export.CSV.zip',
     '217459 0b56900614fbf9f084209a1f949de230 http://data.gdeltproject.org/gdeltv2/20150221140000.mentions.CSV.zip',
     '6325976 6bd6d6dde1169ce6f059b23a9b90e0a2 http://data.gdeltproject.org/gdeltv2/20150221140000.gkg.csv.zip',
     '80879 254d3b881090ec7efc440de3408c67af http://data.gdeltproject.org/gdeltv2/20150221141500.export.CSV.zip',
     '201968 0a3f64fc4b9fc4f50e105415a6af6afd http://data.gdeltproject.org/gdeltv2/20150221141500.mentions.CSV.zip',
     '5415731 41c56adbcbfd3d4edc86a7aef9535dff http://data.gdeltproject.org/gdeltv2/20150221141500.gkg.csv.zip',
     '74558 413de4ffc5bc1460c6db52151d27d896 http://data.gdeltproject.org/gdeltv2/20150221143000.export.CSV.zip',
     '173181 13320f8407aefa7ccce40c3c25a29869 http://data.gdeltproject.org/gdeltv2/20150221143000.mentions.CSV.zip',
     '5301773 6c3e7987c5f5fa9812ad6eeb76100def http://data.gdeltproject.org/gdeltv2/20150221143000.gkg.csv.zip',
     '63281 b0ec6fa7b84f7499294d89742b3e4d1c http://data.gdeltproject.org/gdeltv2/20150221144500.export.CSV.zip',
     '193458 871ca2b4bfd10b983f062026456713ed http://data.gdeltproject.org/gdeltv2/20150221144500.mentions.CSV.zip',
     '5779369 ac443c04a3eab0613020df73d918b942 http://data.gdeltproject.org/gdeltv2/20150221144500.gkg.csv.zip',
     '72560 9aa8a99b55b774d8125ec8113612bcbf http://data.gdeltproject.org/gdeltv2/20150221150000.export.CSV.zip',
     '157956 5a82a4533448f0f82c68066cbe1b67de http://data.gdeltproject.org/gdeltv2/20150221150000.mentions.CSV.zip',
     '5069995 6bbd66d1f3e7e4d2bb1c17d6b27bbd87 http://data.gdeltproject.org/gdeltv2/20150221150000.gkg.csv.zip',
     '71859 1e27260c20764804579a88ab6d70b65d http://data.gdeltproject.org/gdeltv2/20150221151500.export.CSV.zip',
     '166137 1a1f15a8200ee43b4e0c1380a2c1346a http://data.gdeltproject.org/gdeltv2/20150221151500.mentions.CSV.zip',
     '5210203 35937a0289b7f8af0cdd1a77c9d9e3f4 http://data.gdeltproject.org/gdeltv2/20150221151500.gkg.csv.zip',
     '86816 ba0784ed692c0be67a8616c1e726e7fc http://data.gdeltproject.org/gdeltv2/20150221153000.export.CSV.zip',
     '207646 560ba0e6934eeca53754ed18eceeafa2 http://data.gdeltproject.org/gdeltv2/20150221153000.mentions.CSV.zip',
     '6270050 7b5b4b92280c67317a04dee0dc9a1ee7 http://data.gdeltproject.org/gdeltv2/20150221153000.gkg.csv.zip',
     '58899 40d118ceff31311f12b6f304edf1a898 http://data.gdeltproject.org/gdeltv2/20150221154500.export.CSV.zip',
     '148021 224ed2962800df49fcbb9db317dd1f71 http://data.gdeltproject.org/gdeltv2/20150221154500.mentions.CSV.zip',
     '4668558 f5a1db8e82c2dae27d4536d07192b47e http://data.gdeltproject.org/gdeltv2/20150221154500.gkg.csv.zip',
     '59826 83374634901330fc9ae57c1f0270de25 http://data.gdeltproject.org/gdeltv2/20150221160000.export.CSV.zip',
     '127160 3bd19a42c008ad6e4c160be4c51625ee http://data.gdeltproject.org/gdeltv2/20150221160000.mentions.CSV.zip',
     '4042276 df3c3c74cf4415d1f5ee452f88d2ef5a http://data.gdeltproject.org/gdeltv2/20150221160000.gkg.csv.zip',
     '77475 326d301f8628ca2196b8ab5abcf663ce http://data.gdeltproject.org/gdeltv2/20150221161500.export.CSV.zip',
     '195230 8d64497713a126636475ac19f2813fd3 http://data.gdeltproject.org/gdeltv2/20150221161500.mentions.CSV.zip',
     '5879941 0f2f87507399002b81565033791575b4 http://data.gdeltproject.org/gdeltv2/20150221161500.gkg.csv.zip',
     '75628 fcdecd2feb2ac1508ede30e8f4d01680 http://data.gdeltproject.org/gdeltv2/20150221163000.export.CSV.zip',
     '165576 c6b8d62a845b85904b2baad7db603bce http://data.gdeltproject.org/gdeltv2/20150221163000.mentions.CSV.zip',
     '5816219 6a3556f18b66b6ef34a982d0b2b5a8c2 http://data.gdeltproject.org/gdeltv2/20150221163000.gkg.csv.zip',
     '73586 f1e6c7227338d385d7458fe75b5dffa6 http://data.gdeltproject.org/gdeltv2/20150221164500.export.CSV.zip',
     '148679 a83f4b1ea7c1d1e0c442aec997f92ccb http://data.gdeltproject.org/gdeltv2/20150221164500.mentions.CSV.zip',
     '5014410 0a7aeba2231bc9e8e2054fae44f81fac http://data.gdeltproject.org/gdeltv2/20150221164500.gkg.csv.zip',
     '80179 284685ea379fdae20466bf23dd702fb5 http://data.gdeltproject.org/gdeltv2/20150221170000.export.CSV.zip',
     '162845 acb53c7cff2eb54d7ef60b8477857e67 http://data.gdeltproject.org/gdeltv2/20150221170000.mentions.CSV.zip',
     '5432047 c36ea8ca824317bc270d828a750d1ecc http://data.gdeltproject.org/gdeltv2/20150221170000.gkg.csv.zip',
     '60968 3ea35fc9af629ac21627b105f6cfed34 http://data.gdeltproject.org/gdeltv2/20150221171500.export.CSV.zip',
     '147843 8cdf388f182632f0d412666500113ed4 http://data.gdeltproject.org/gdeltv2/20150221171500.mentions.CSV.zip',
     '4782800 bb934b0c0035c8d0d22e9a19d4d3510a http://data.gdeltproject.org/gdeltv2/20150221171500.gkg.csv.zip',
     '72896 c878ab48ad789cf4ae3a8b9938e7520a http://data.gdeltproject.org/gdeltv2/20150221173000.export.CSV.zip',
     '161351 e7055529bfdce317cabda6a0462e6b8a http://data.gdeltproject.org/gdeltv2/20150221173000.mentions.CSV.zip',
     '5126405 25d45ac3de54ee4ba386e7ba23ee9db7 http://data.gdeltproject.org/gdeltv2/20150221173000.gkg.csv.zip',
     '90240 12eb0eed9926c75289f0d0cb36608915 http://data.gdeltproject.org/gdeltv2/20150221174500.export.CSV.zip',
     '181089 9f1391c7ed803de4a2bea9f2f0f0fb6f http://data.gdeltproject.org/gdeltv2/20150221174500.mentions.CSV.zip',
     '6215175 034e33a6d16c6d72e6c81376f08dad96 http://data.gdeltproject.org/gdeltv2/20150221174500.gkg.csv.zip',
     '92741 f3597a8cb248e1751648134a806d8556 http://data.gdeltproject.org/gdeltv2/20150221180000.export.CSV.zip',
     '162074 e4d65dabe8039abc1bd7ec49b0fd916a http://data.gdeltproject.org/gdeltv2/20150221180000.mentions.CSV.zip',
     '5718872 62c73d70d96c1dd7cb937967fc2bc9d3 http://data.gdeltproject.org/gdeltv2/20150221180000.gkg.csv.zip',
     '74219 6a1168c27e87f7e3361af007b1c18925 http://data.gdeltproject.org/gdeltv2/20150221181500.export.CSV.zip',
     '173093 21eb8252020bcf8fe896073bcfd50318 http://data.gdeltproject.org/gdeltv2/20150221181500.mentions.CSV.zip',
     '5509731 87cae8ec9858b0dcdf911a6b95639424 http://data.gdeltproject.org/gdeltv2/20150221181500.gkg.csv.zip',
     '75336 62a113af33b68c6207c1f6404312d894 http://data.gdeltproject.org/gdeltv2/20150221183000.export.CSV.zip',
     '166665 6644c66793f38113ff26327033307107 http://data.gdeltproject.org/gdeltv2/20150221183000.mentions.CSV.zip',
     '5848425 be9f2a333f9e1419af56edd0f7be4719 http://data.gdeltproject.org/gdeltv2/20150221183000.gkg.csv.zip',
     '65360 e623f65ef71303c18a3c38ea37002b4d http://data.gdeltproject.org/gdeltv2/20150221184500.export.CSV.zip',
     '160989 990b9fbe9c9ef09be64e3c77c240e895 http://data.gdeltproject.org/gdeltv2/20150221184500.mentions.CSV.zip',
     '5275246 c26d98ed9250f94b0d4cb2e429dab81f http://data.gdeltproject.org/gdeltv2/20150221184500.gkg.csv.zip',
     '98546 7370bf12ad87b8af5e7d1e626d407be1 http://data.gdeltproject.org/gdeltv2/20150221190000.export.CSV.zip',
     '186307 a54cdd51dab0d131c469b6985eee834f http://data.gdeltproject.org/gdeltv2/20150221190000.mentions.CSV.zip',
     '5792964 277968be5b847ef04672c34d16bec1eb http://data.gdeltproject.org/gdeltv2/20150221190000.gkg.csv.zip',
     '76378 dfeb7eb2c875062574dde016f4f8b57c http://data.gdeltproject.org/gdeltv2/20150221191500.export.CSV.zip',
     '177435 9f0ba013f154fb325e57ed12861b2e58 http://data.gdeltproject.org/gdeltv2/20150221191500.mentions.CSV.zip',
     '5100400 e62a33a2ea7134f1864746d2be35b80b http://data.gdeltproject.org/gdeltv2/20150221191500.gkg.csv.zip',
     '84077 706167f13d639630917429b053009162 http://data.gdeltproject.org/gdeltv2/20150221193000.export.CSV.zip',
     '177365 21619442b1bb749b14ca65c8aa01de7d http://data.gdeltproject.org/gdeltv2/20150221193000.mentions.CSV.zip',
     '5369099 1fb676d27d2be46a82a9125ba4ddf06d http://data.gdeltproject.org/gdeltv2/20150221193000.gkg.csv.zip',
     '70892 fe671d83748545fe2d96c60ffb54cc18 http://data.gdeltproject.org/gdeltv2/20150221194500.export.CSV.zip',
     '158899 70568e6390b570d77a5efe6271601fe6 http://data.gdeltproject.org/gdeltv2/20150221194500.mentions.CSV.zip',
     '5061426 00bd22269a5b5f458b1efe577334a3fd http://data.gdeltproject.org/gdeltv2/20150221194500.gkg.csv.zip',
     '64064 ce09aa0e0f90a8514f0de226af198bfb http://data.gdeltproject.org/gdeltv2/20150221200000.export.CSV.zip',
     '160782 199591b829633980eb53b34f0f1a6b29 http://data.gdeltproject.org/gdeltv2/20150221200000.mentions.CSV.zip',
     '5179859 40df72cbf0afd9a2a6dead0b13f4277c http://data.gdeltproject.org/gdeltv2/20150221200000.gkg.csv.zip',
     '74698 ff056df63b3d78200411bf0648ae0eba http://data.gdeltproject.org/gdeltv2/20150221201500.export.CSV.zip',
     '145553 4510ff74e63bb73ed41ecb1f3218d9f5 http://data.gdeltproject.org/gdeltv2/20150221201500.mentions.CSV.zip',
     '4759207 e2ca40aed424ab85a8a84aa2db861a61 http://data.gdeltproject.org/gdeltv2/20150221201500.gkg.csv.zip',
     '76222 f3738232d53a9f1203f91be470b16d28 http://data.gdeltproject.org/gdeltv2/20150221203000.export.CSV.zip',
     '170678 774e740e1dc2231e5dbb27b586e49118 http://data.gdeltproject.org/gdeltv2/20150221203000.mentions.CSV.zip',
     '4772470 8ee676236b2cd2a55bf481fcfded3ed7 http://data.gdeltproject.org/gdeltv2/20150221203000.gkg.csv.zip',
     '70509 4dbf9c5eea8032c673fed27f870f9c0f http://data.gdeltproject.org/gdeltv2/20150221204500.export.CSV.zip',
     '169443 c7db1a4237d2720e8db8248b39b0579e http://data.gdeltproject.org/gdeltv2/20150221204500.mentions.CSV.zip',
     '5126422 ab79442b72c9d8e054ca28165956a887 http://data.gdeltproject.org/gdeltv2/20150221204500.gkg.csv.zip',
     '66457 17ef4578429490feffd28d11c85c2a43 http://data.gdeltproject.org/gdeltv2/20150221210000.export.CSV.zip',
     '159157 17912fd0b37b2a812c7bf6dde1d31788 http://data.gdeltproject.org/gdeltv2/20150221210000.mentions.CSV.zip',
     '4771612 89e57cddb3c7a6965b1fbb44d3efc061 http://data.gdeltproject.org/gdeltv2/20150221210000.gkg.csv.zip',
     '62976 e91c327abd3f89919ca8b95e87f3f80a http://data.gdeltproject.org/gdeltv2/20150221211500.export.CSV.zip',
     '138508 ec09ad8e24d01402f6cf4537b0a635f7 http://data.gdeltproject.org/gdeltv2/20150221211500.mentions.CSV.zip',
     '4508151 aecea2620e458d720b207bdfd066ea9b http://data.gdeltproject.org/gdeltv2/20150221211500.gkg.csv.zip',
     '75769 0ddb2ee984d6bb9cb884af44521280f4 http://data.gdeltproject.org/gdeltv2/20150221213000.export.CSV.zip',
     '179101 df2633d22f66d31f180d0ffc4eb74046 http://data.gdeltproject.org/gdeltv2/20150221213000.mentions.CSV.zip',
     '5870006 71e487f40f432dc772079d50c1ba7b27 http://data.gdeltproject.org/gdeltv2/20150221213000.gkg.csv.zip',
     '64080 35cbc130ae0c0333a6d955b85cb2bb72 http://data.gdeltproject.org/gdeltv2/20150221214500.export.CSV.zip',
     '149919 03a766a6725435d92b2155984ca1f141 http://data.gdeltproject.org/gdeltv2/20150221214500.mentions.CSV.zip',
     '4811814 c5286162b1cb17b3441389446ea9895d http://data.gdeltproject.org/gdeltv2/20150221214500.gkg.csv.zip',
     '66636 02119b3ff57f265cc4443b042c04ffbf http://data.gdeltproject.org/gdeltv2/20150221220000.export.CSV.zip',
     '135681 1252a18b5acdca7e4d1efd9a07226fd2 http://data.gdeltproject.org/gdeltv2/20150221220000.mentions.CSV.zip',
     '4827577 9a286feaa2028f5374bd0cbfc46e2ad6 http://data.gdeltproject.org/gdeltv2/20150221220000.gkg.csv.zip',
     '64446 f010033d8502ccd624e518af25211cb9 http://data.gdeltproject.org/gdeltv2/20150221221500.export.CSV.zip',
     '161068 471d383585a5beecc56206b3482d4450 http://data.gdeltproject.org/gdeltv2/20150221221500.mentions.CSV.zip',
     '4683780 fe9a366cbf90f7ecab71f24c06252437 http://data.gdeltproject.org/gdeltv2/20150221221500.gkg.csv.zip',
     '78300 6c78f5209b24908eefbed192881c1b64 http://data.gdeltproject.org/gdeltv2/20150221223000.export.CSV.zip',
     '162978 dedf6e2ef6943f6c9c5b9534c2e7635a http://data.gdeltproject.org/gdeltv2/20150221223000.mentions.CSV.zip',
     '5704810 70054a7f66a8e423f2eb6120b74939d5 http://data.gdeltproject.org/gdeltv2/20150221223000.gkg.csv.zip',
     '55384 dad5ce0e541c413ff7fcb578e2f7a04f http://data.gdeltproject.org/gdeltv2/20150221224500.export.CSV.zip',
     '124031 0af8f9c1a6be27073f4291b17e5484dd http://data.gdeltproject.org/gdeltv2/20150221224500.mentions.CSV.zip',
     '4956244 4e5f3cfcfacdc7498e844a3ded7d8fff http://data.gdeltproject.org/gdeltv2/20150221224500.gkg.csv.zip',
     '79861 3f6c3e38fdb857919a8c552fb511ba01 http://data.gdeltproject.org/gdeltv2/20150221230000.export.CSV.zip',
     '151870 1cae7305a58b43097e30b76e1bd5af8a http://data.gdeltproject.org/gdeltv2/20150221230000.mentions.CSV.zip',
     '5819324 14dbbb57929b5270600889af9f18b03a http://data.gdeltproject.org/gdeltv2/20150221230000.gkg.csv.zip',
     '64038 a9e2f7da0e319994bdf226b04c40dd07 http://data.gdeltproject.org/gdeltv2/20150221231500.export.CSV.zip',
     '135245 4707424363008a7b9a109de09508adbb http://data.gdeltproject.org/gdeltv2/20150221231500.mentions.CSV.zip',
     '5068042 888165073d913106d9c5ea769628d507 http://data.gdeltproject.org/gdeltv2/20150221231500.gkg.csv.zip',
     '63086 bfe2233c5ad35584616e96211138b396 http://data.gdeltproject.org/gdeltv2/20150221233000.export.CSV.zip',
     '127005 22c58ce401cb179438dd72f7af355b49 http://data.gdeltproject.org/gdeltv2/20150221233000.mentions.CSV.zip',
     '5246294 8a0fbf460d1b9a96a7dec420f658e7b5 http://data.gdeltproject.org/gdeltv2/20150221233000.gkg.csv.zip',
     '58022 e78ad9b442c33af3c8d3b9c98e1f22bc http://data.gdeltproject.org/gdeltv2/20150221234500.export.CSV.zip',
     '154787 f54192b95f4bae3adb8c5a83a5d89279 http://data.gdeltproject.org/gdeltv2/20150221234500.mentions.CSV.zip',
     '6137850 dbfec3fdd5e7b6e2ffe3b3f0b56d4b3d http://data.gdeltproject.org/gdeltv2/20150221234500.gkg.csv.zip',
     '145342 48b628b9f796947af24f9265776f566a http://data.gdeltproject.org/gdeltv2/20150222000000.export.CSV.zip',
     '109666 876485e270046584d0c84de8ba03bd38 http://data.gdeltproject.org/gdeltv2/20150222000000.mentions.CSV.zip',
     '4691928 f8c42a997b924976930330cd2c7f5c9f http://data.gdeltproject.org/gdeltv2/20150222000000.gkg.csv.zip',
     '147614 089d34826d93ad4d6b5d64e3ea768eb7 http://data.gdeltproject.org/gdeltv2/20150222001500.export.CSV.zip',
     '118608 504b311e4ee1b44f66e2ce1310f93e18 http://data.gdeltproject.org/gdeltv2/20150222001500.mentions.CSV.zip',
     '4645150 d7b45976ec019527aa1b821bb8d483d8 http://data.gdeltproject.org/gdeltv2/20150222001500.gkg.csv.zip',
     '161639 a936077d6393be840018db2a1d7acd68 http://data.gdeltproject.org/gdeltv2/20150222003000.export.CSV.zip',
     '150598 3da791577dd57309887e6b0c57abc5eb http://data.gdeltproject.org/gdeltv2/20150222003000.mentions.CSV.zip',
     '6058345 14126fbe7f150a44bddc4a4d6d17b247 http://data.gdeltproject.org/gdeltv2/20150222003000.gkg.csv.zip',
     '131371 419660fcc6bbeb1f6edcffc1d96bd23d http://data.gdeltproject.org/gdeltv2/20150222004500.export.CSV.zip',
     '145167 20a031f6707f3957df9b551c7c53e9bb http://data.gdeltproject.org/gdeltv2/20150222004500.mentions.CSV.zip',
     '5145479 7d7ee26a40a69302402a04e5b343249f http://data.gdeltproject.org/gdeltv2/20150222004500.gkg.csv.zip',
     '92247 84e14a9bac8ec65ee2b80050fb841b4a http://data.gdeltproject.org/gdeltv2/20150222010000.export.CSV.zip',
     '101226 0711ca936be3d68f18055329596cd827 http://data.gdeltproject.org/gdeltv2/20150222010000.mentions.CSV.zip',
     '4446362 6f689d8c853943705586f9f096409335 http://data.gdeltproject.org/gdeltv2/20150222010000.gkg.csv.zip',
     '97476 61213192be8e8aa0e6cad8298630122b http://data.gdeltproject.org/gdeltv2/20150222011500.export.CSV.zip',
     '113698 473a60a8a77517ef101e320eebf3b580 http://data.gdeltproject.org/gdeltv2/20150222011500.mentions.CSV.zip',
     '4486413 18b56d4eb35031216621012c8aa735e9 http://data.gdeltproject.org/gdeltv2/20150222011500.gkg.csv.zip',
     '89619 3291740ede3011d774dd10720ee572cc http://data.gdeltproject.org/gdeltv2/20150222013000.export.CSV.zip',
     '104433 bcf931244891c7382bd017dec25402cf http://data.gdeltproject.org/gdeltv2/20150222013000.mentions.CSV.zip',
     '4461399 f77d4ee45d852c1699104b7adfd2e9e2 http://data.gdeltproject.org/gdeltv2/20150222013000.gkg.csv.zip',
     '68726 dfc84e10cd7fdc8c4f4c41f796f68a6a http://data.gdeltproject.org/gdeltv2/20150222014500.export.CSV.zip',
     '95127 020d4331e50abcd58ed04aec129699be http://data.gdeltproject.org/gdeltv2/20150222014500.mentions.CSV.zip',
     '3498182 5cbd32f88bc24a70faf5eaecd28ef1b6 http://data.gdeltproject.org/gdeltv2/20150222014500.gkg.csv.zip',
     '90985 b3b0d7b36160cabcd585b01c894feccc http://data.gdeltproject.org/gdeltv2/20150222020000.export.CSV.zip',
     '114855 e68e3232c4e03cbfab885429f52ffb2b http://data.gdeltproject.org/gdeltv2/20150222020000.mentions.CSV.zip',
     '4488797 6f2fc1625c9a9f20612f993f28dfe4c2 http://data.gdeltproject.org/gdeltv2/20150222020000.gkg.csv.zip',
     '91110 9d458cc598e929ea71e40b2adfae85f0 http://data.gdeltproject.org/gdeltv2/20150222021500.export.CSV.zip',
     '116376 80f6bd7c8e99fa83188c83727e32eecf http://data.gdeltproject.org/gdeltv2/20150222021500.mentions.CSV.zip',
     '4461421 95e3a0f99d557886fe8ee416c1f6f715 http://data.gdeltproject.org/gdeltv2/20150222021500.gkg.csv.zip',
     '113987 2e6ab77bfe8f23e78df08cbff7f7ce26 http://data.gdeltproject.org/gdeltv2/20150222023000.export.CSV.zip',
     '122993 71a0375e7b9b8f33357299b713b35c2e http://data.gdeltproject.org/gdeltv2/20150222023000.mentions.CSV.zip',
     '4153879 63e7b16052288cbef122b461e96fb84b http://data.gdeltproject.org/gdeltv2/20150222023000.gkg.csv.zip',
     '145991 aae9f650e4669a5e5aed51c028b7162d http://data.gdeltproject.org/gdeltv2/20150222024500.export.CSV.zip',
     '164530 31478e87dac1a6dcac40e665d4dff10a http://data.gdeltproject.org/gdeltv2/20150222024500.mentions.CSV.zip',
     '6679323 0ee96c2d1a9cd615dcf7477fd03b8d71 http://data.gdeltproject.org/gdeltv2/20150222024500.gkg.csv.zip',
     '78579 e14e7a9526f47993f71964c7191cfc9c http://data.gdeltproject.org/gdeltv2/20150222030000.export.CSV.zip',
     '105899 e276d4f8f137654254ea736247f502a5 http://data.gdeltproject.org/gdeltv2/20150222030000.mentions.CSV.zip',
     '4596088 8d8bc8d0e5d8e2c2f4d96b3a0fbb72d7 http://data.gdeltproject.org/gdeltv2/20150222030000.gkg.csv.zip',
     '91138 336508128dc858c440e87a04528b77d4 http://data.gdeltproject.org/gdeltv2/20150222031500.export.CSV.zip',
     '111196 841f505617c24f4596531c065d907ba7 http://data.gdeltproject.org/gdeltv2/20150222031500.mentions.CSV.zip',
     '4194961 cfd05a297f1f36912972a37c05f94653 http://data.gdeltproject.org/gdeltv2/20150222031500.gkg.csv.zip',
     '83473 20ea602bd9a16e466c7411c56fd09e5d http://data.gdeltproject.org/gdeltv2/20150222033000.export.CSV.zip',
     '128462 0b8b580b337ae317028d598c105a0348 http://data.gdeltproject.org/gdeltv2/20150222033000.mentions.CSV.zip',
     '5033114 814ce962cad2c8f58e8b080b0d014beb http://data.gdeltproject.org/gdeltv2/20150222033000.gkg.csv.zip',
     '73827 a9b31e712481fd93be4ae6dcfc0ea45c http://data.gdeltproject.org/gdeltv2/20150222034500.export.CSV.zip',
     '111879 ce588bd1a8b0f516316615999988f8a1 http://data.gdeltproject.org/gdeltv2/20150222034500.mentions.CSV.zip',
     '4937996 65fee25c87f2a52e3f44d0d03084b5d6 http://data.gdeltproject.org/gdeltv2/20150222034500.gkg.csv.zip',
     '84851 3412bfa35b600ea453f47f58c4ac3073 http://data.gdeltproject.org/gdeltv2/20150222040000.export.CSV.zip',
     '127386 400154bfe86deaf1a82159a031457a95 http://data.gdeltproject.org/gdeltv2/20150222040000.mentions.CSV.zip',
     '5128402 9a2ad1c729105a8dfcfadd16389465ea http://data.gdeltproject.org/gdeltv2/20150222040000.gkg.csv.zip',
     '73103 5e45163a127efcc3ab8e01bfec6d0b0f http://data.gdeltproject.org/gdeltv2/20150222043000.export.CSV.zip',
     '98876 d62e49596e551516541011bcab51b5cc http://data.gdeltproject.org/gdeltv2/20150222043000.mentions.CSV.zip',
     '4118381 2371534365b38964391c1762d31d47a4 http://data.gdeltproject.org/gdeltv2/20150222043000.gkg.csv.zip',
     '73197 336d10ae0994f2c4a661d863dd4b81ba http://data.gdeltproject.org/gdeltv2/20150222041500.export.CSV.zip',
     '115656 3caaacef46ad5b70fa047887c64faad9 http://data.gdeltproject.org/gdeltv2/20150222041500.mentions.CSV.zip',
     '4496171 8c0a173764d65c6ab16f2db084a68932 http://data.gdeltproject.org/gdeltv2/20150222041500.gkg.csv.zip',
     '81152 1951258722d59eff0f77f16526d03bfb http://data.gdeltproject.org/gdeltv2/20150222044500.export.CSV.zip',
     '120127 11404712c9364eb12384a3163bdb0bfd http://data.gdeltproject.org/gdeltv2/20150222044500.mentions.CSV.zip',
     '4746259 9ea481819208f8df14795b9f3077972c http://data.gdeltproject.org/gdeltv2/20150222044500.gkg.csv.zip',
     '74031 df57aad82181b089d479c47dd8ebd4ea http://data.gdeltproject.org/gdeltv2/20150222050000.export.CSV.zip',
     '120429 7327dbfdf6bb49a74b28ebfd9eb2bb3d http://data.gdeltproject.org/gdeltv2/20150222050000.mentions.CSV.zip',
     '4764358 18ae77e8292e5218c32835950385b969 http://data.gdeltproject.org/gdeltv2/20150222050000.gkg.csv.zip',
     '83197 c3b750a4445c478e1e5b5c62804f9b4c http://data.gdeltproject.org/gdeltv2/20150222051500.export.CSV.zip',
     '117998 4973c535c74c6733a249e84ebbc4ebd6 http://data.gdeltproject.org/gdeltv2/20150222051500.mentions.CSV.zip',
     '4702027 b77f319440cc70fd1a9d370c01e1c275 http://data.gdeltproject.org/gdeltv2/20150222051500.gkg.csv.zip',
     '97304 6906dea8eeccb187db4093545db7f89b http://data.gdeltproject.org/gdeltv2/20150222053000.export.CSV.zip',
     '126824 5a8a9196d7bbdc6baeb1c9f3a8561b00 http://data.gdeltproject.org/gdeltv2/20150222053000.mentions.CSV.zip',
     '4992915 27b7c2c56533df07e81aa3d5bb47dff4 http://data.gdeltproject.org/gdeltv2/20150222053000.gkg.csv.zip',
     '99233 01b270b94c83a5db659ca9e8a5792170 http://data.gdeltproject.org/gdeltv2/20150222054500.export.CSV.zip',
     '141656 e32d822bdae3c912052d0f8bc9a1ff4c http://data.gdeltproject.org/gdeltv2/20150222054500.mentions.CSV.zip',
     '5319282 cf74aa1a4ba999936e9146566d561d70 http://data.gdeltproject.org/gdeltv2/20150222054500.gkg.csv.zip',
     '53505 d3afd5f7bc2d9d191911c9ce6437ed27 http://data.gdeltproject.org/gdeltv2/20150222060000.export.CSV.zip',
     '87237 bedd89f82ed7bbd2d213216e5742f43c http://data.gdeltproject.org/gdeltv2/20150222060000.mentions.CSV.zip',
     '3981366 b02171f8305bf1da404c3c8dd1e25f4e http://data.gdeltproject.org/gdeltv2/20150222060000.gkg.csv.zip',
     '74166 91540373f09419be957829ea43721e4f http://data.gdeltproject.org/gdeltv2/20150222061500.export.CSV.zip',
     '104250 ce3d38dcbeef2532947ca0e7d0263d87 http://data.gdeltproject.org/gdeltv2/20150222061500.mentions.CSV.zip',
     '4253103 e330f45a3abcf1b407f1bf7732e88094 http://data.gdeltproject.org/gdeltv2/20150222061500.gkg.csv.zip',
     '83486 f6101338891b97296cb7367f0bfae336 http://data.gdeltproject.org/gdeltv2/20150222063000.export.CSV.zip',
     '142780 2cc6e7a30d10d407e830a73ad75e14c5 http://data.gdeltproject.org/gdeltv2/20150222063000.mentions.CSV.zip',
     '5098223 03314a2ebed76a40b629f2c7b4988a60 http://data.gdeltproject.org/gdeltv2/20150222063000.gkg.csv.zip',
     '63641 c02093cc193c408f042d3a9fc2930f58 http://data.gdeltproject.org/gdeltv2/20150222064500.export.CSV.zip',
     '110045 e7d3f687899e6942edea710961fa071b http://data.gdeltproject.org/gdeltv2/20150222064500.mentions.CSV.zip',
     '4986589 6214983934c406af11ed18f2908b4028 http://data.gdeltproject.org/gdeltv2/20150222064500.gkg.csv.zip',
     '74620 39531b4f32db4adcb87eb6c97ca7caa9 http://data.gdeltproject.org/gdeltv2/20150222070000.export.CSV.zip',
     '132569 ce3fa197b53491a0bfbd6c4ccc1de953 http://data.gdeltproject.org/gdeltv2/20150222070000.mentions.CSV.zip',
     '5090436 6d48c024537ccf82ea65571480b830fe http://data.gdeltproject.org/gdeltv2/20150222070000.gkg.csv.zip',
     '77335 e17c563065921eb831a033e0545b542a http://data.gdeltproject.org/gdeltv2/20150222071500.export.CSV.zip',
     '132282 dad636daa851aa99a68f50ecc0e43897 http://data.gdeltproject.org/gdeltv2/20150222071500.mentions.CSV.zip',
     '5297066 210b8562f8ea037b0f83ccbb6fe12ad1 http://data.gdeltproject.org/gdeltv2/20150222071500.gkg.csv.zip',
     '95040 b99fe6eddf076caecfeeae61f72e6cf8 http://data.gdeltproject.org/gdeltv2/20150222073000.export.CSV.zip',
     '141159 96000721112357bfb4cad0c79af6fcec http://data.gdeltproject.org/gdeltv2/20150222073000.mentions.CSV.zip',
     '5084596 f290a59395f453f508a3382bfe3420e2 http://data.gdeltproject.org/gdeltv2/20150222073000.gkg.csv.zip',
     '74973 b432b6909b78fb604b91cdc70b0393f4 http://data.gdeltproject.org/gdeltv2/20150222074500.export.CSV.zip',
     '120885 b90419a3bfc2316e7863270d4b16dfc0 http://data.gdeltproject.org/gdeltv2/20150222074500.mentions.CSV.zip',
     '4422561 d97400045102ce23046ef3c02a8ae7a0 http://data.gdeltproject.org/gdeltv2/20150222074500.gkg.csv.zip',
     '72107 16caffcaeb57dba75db4b8b91cc240e8 http://data.gdeltproject.org/gdeltv2/20150222080000.export.CSV.zip',
     '131774 5daecc46a446eaa7accdfbd6586e91a7 http://data.gdeltproject.org/gdeltv2/20150222080000.mentions.CSV.zip',
     '5200273 e3d9b7ff86aee7d0abf1583fd1b857c0 http://data.gdeltproject.org/gdeltv2/20150222080000.gkg.csv.zip',
     '67612 0cabcc41d3fea5ff7846a2b20d2724ba http://data.gdeltproject.org/gdeltv2/20150222081500.export.CSV.zip',
     '121952 e6f6aab353dbd05b47df15a2220acd2a http://data.gdeltproject.org/gdeltv2/20150222081500.mentions.CSV.zip',
     '4212642 1240047835b2372aaec695c20336c5c1 http://data.gdeltproject.org/gdeltv2/20150222081500.gkg.csv.zip',
     '83473 b8a28510eaa930c06f3c93d2b85d97d3 http://data.gdeltproject.org/gdeltv2/20150222083000.export.CSV.zip',
     '147521 7b2b3efa8f25d5e8cf73fb731a9063df http://data.gdeltproject.org/gdeltv2/20150222083000.mentions.CSV.zip',
     '5854404 2236d9662d98d75495535ab8152517da http://data.gdeltproject.org/gdeltv2/20150222083000.gkg.csv.zip',
     '82810 888db5c09b4fb60382a19f1c8cda36a8 http://data.gdeltproject.org/gdeltv2/20150222084500.export.CSV.zip',
     '135503 9faae7cb20da76f43cbf593540f694fc http://data.gdeltproject.org/gdeltv2/20150222084500.mentions.CSV.zip',
     '5470742 306c6bdf13f8732ab102b768ea8139e3 http://data.gdeltproject.org/gdeltv2/20150222084500.gkg.csv.zip',
     '66983 bd039a95195964f367e5060ed127e33e http://data.gdeltproject.org/gdeltv2/20150222090000.export.CSV.zip',
     '108992 d166bc9e776233fcd917cba6e64dd4f0 http://data.gdeltproject.org/gdeltv2/20150222090000.mentions.CSV.zip',
     '4384747 42edd3eb09a656d71d202ad426e1b402 http://data.gdeltproject.org/gdeltv2/20150222090000.gkg.csv.zip',
     '65083 6873320ac30dbe8413eb6be91d69f4f4 http://data.gdeltproject.org/gdeltv2/20150222091500.export.CSV.zip',
     '112086 bb1c25a2a1a0e62e2f736629ac7e07f2 http://data.gdeltproject.org/gdeltv2/20150222091500.mentions.CSV.zip',
     '4183546 3db383a9a85ece126fda5ce463428b02 http://data.gdeltproject.org/gdeltv2/20150222091500.gkg.csv.zip',
     '99561 3872f0cb3d7970d6b11abe236ac4f5bb http://data.gdeltproject.org/gdeltv2/20150222093000.export.CSV.zip',
     '143348 c00a259b1e6f6edc05afa99ea19b9479 http://data.gdeltproject.org/gdeltv2/20150222093000.mentions.CSV.zip',
     '5264249 3513864eff02034e4bbb6d2da6767dbc http://data.gdeltproject.org/gdeltv2/20150222093000.gkg.csv.zip',
     '66474 9165bfdcfc1510593aa22a9985bbbe39 http://data.gdeltproject.org/gdeltv2/20150222094500.export.CSV.zip',
     '115149 b39d3e76b10806484ba23928af049587 http://data.gdeltproject.org/gdeltv2/20150222094500.mentions.CSV.zip',
     '4371208 23a543cf2a6743e9ea2e1895cdc4f841 http://data.gdeltproject.org/gdeltv2/20150222094500.gkg.csv.zip',
     '85766 179b1559324cd0488c476576209232d0 http://data.gdeltproject.org/gdeltv2/20150222100000.export.CSV.zip',
     '132385 77cd37f575fabdf1daf9c271757c54be http://data.gdeltproject.org/gdeltv2/20150222100000.mentions.CSV.zip',
     '4713595 5821964f6f10e7512d20f8e44e3b9a9b http://data.gdeltproject.org/gdeltv2/20150222100000.gkg.csv.zip',
     '55154 bd95776381bb8d2585c48abf860d48c0 http://data.gdeltproject.org/gdeltv2/20150222101500.export.CSV.zip',
     '120984 85be450936f7ca5292d4a8d9befae335 http://data.gdeltproject.org/gdeltv2/20150222101500.mentions.CSV.zip',
     '4117452 85406d5fb89dcc5b32224c03f0c53df3 http://data.gdeltproject.org/gdeltv2/20150222101500.gkg.csv.zip',
     '80017 e80ddee8d3662b9c1d13eab4c2db847e http://data.gdeltproject.org/gdeltv2/20150222103000.export.CSV.zip',
     '122921 243ea5bc6bab612c8736689acb2459f2 http://data.gdeltproject.org/gdeltv2/20150222103000.mentions.CSV.zip',
     '4396535 4789fec9ff9d3fc849b4d9c10fe2df8f http://data.gdeltproject.org/gdeltv2/20150222103000.gkg.csv.zip',
     '77928 3a1309c6bc2475c13bf2c4f82771c1d9 http://data.gdeltproject.org/gdeltv2/20150222104500.export.CSV.zip',
     '124131 9dabe275e6f54972dbd305a7e2f4fd04 http://data.gdeltproject.org/gdeltv2/20150222104500.mentions.CSV.zip',
     '4073052 2372eb7d17f6e75bf58feece070d8d42 http://data.gdeltproject.org/gdeltv2/20150222104500.gkg.csv.zip',
     '59473 c766c299f55e869f640d31f0c8c39cf3 http://data.gdeltproject.org/gdeltv2/20150222110000.export.CSV.zip',
     '108464 63bcfe4d4936b66a52c232e84c6ef0e8 http://data.gdeltproject.org/gdeltv2/20150222110000.mentions.CSV.zip',
     '3806437 716daba89d59fdda406673184428d262 http://data.gdeltproject.org/gdeltv2/20150222110000.gkg.csv.zip',
     '58338 429af1c2b0de1e0851c18aeb1404a968 http://data.gdeltproject.org/gdeltv2/20150222111500.export.CSV.zip',
     '108176 797820db41ad124a632827be40470b85 http://data.gdeltproject.org/gdeltv2/20150222111500.mentions.CSV.zip',
     '3490612 3559b1b671ba1468718ae28247b674ef http://data.gdeltproject.org/gdeltv2/20150222111500.gkg.csv.zip',
     '64508 22d3fc5d7aaf9d8d06571d0f3815a573 http://data.gdeltproject.org/gdeltv2/20150222113000.export.CSV.zip',
     '117996 409a6f3dd55a1f9e3e29f368866e7e33 http://data.gdeltproject.org/gdeltv2/20150222113000.mentions.CSV.zip',
     '3738791 4b9ef5c03eae5fb7d523d4cb0c87da95 http://data.gdeltproject.org/gdeltv2/20150222113000.gkg.csv.zip',
     '59613 00463de52c2698f0d30e218b353892c1 http://data.gdeltproject.org/gdeltv2/20150222114500.export.CSV.zip',
     '126817 ad653b8788730fee089addf849d0c45f http://data.gdeltproject.org/gdeltv2/20150222114500.mentions.CSV.zip',
     '4221941 9b38c90ba2c8d6845e24329507995d0e http://data.gdeltproject.org/gdeltv2/20150222114500.gkg.csv.zip',
     '49487 a994b7787d90e52d09567d749b96e1ac http://data.gdeltproject.org/gdeltv2/20150222120000.export.CSV.zip',
     '86537 cb3fb27c5487ad133503d7ad0765c1ee http://data.gdeltproject.org/gdeltv2/20150222120000.mentions.CSV.zip',
     '3658117 a66a785e94ca18afa051457bae8861a6 http://data.gdeltproject.org/gdeltv2/20150222120000.gkg.csv.zip',
     '75276 0b89222f97627b8f7c7093c6ccf34de9 http://data.gdeltproject.org/gdeltv2/20150222121500.export.CSV.zip',
     ...]




```python
import pandas as pd

pd.options.display.max_rows = 200
# df = pd.DataFrame(data.json())
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-6-b2a93ce87bd3> in <module>()
          2 
          3 pd.options.display.max_rows = 200
    ----> 4 df = pd.DataFrame(data.json())
    

    NameError: name 'data' is not defined



```python
df['coords'] = df.features.apply(lambda row: row['geometry']['coordinates'])
df['lat'] = df.features.apply(lambda row: row['geometry']['coordinates'][1])
df['lon'] = df.features.apply(lambda row: row['geometry']['coordinates'][0])
df['name'] = df.features.apply(lambda row: row['properties']['name'])
df['pubdate'] = df.features.apply(lambda row: row['properties']['urlpubtimedate'])
df['urltone'] = df.features.apply(lambda row: row['properties']['urltone'])
df['mentionedNames'] = df.features.apply(lambda row: row['properties']['mentionednames'])
df['mentioinedThemes'] = df.features.apply(lambda row: row['properties']['mentionedthemes'])
df['url'] = df.features.apply(lambda row: row['properties']['url'])
```

# GDELT 2.0 Access


```python
import requests
masterListUrl = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
directory = requests.get(masterListUrl)
clean = directory.content.split('\n')
clean = map(lambda x: x.split(' '),clean)
```

# Logic for GDELT module

Enter a date
* default is take current time and most recent file
* enter historical date; defaults to no time specificity
    * parse
    * add feature to enter time for historical and pull closest 15 minute file
    
choose a database
*  Select between events, event mentions or gkg

return it as a python or R dataframe
*  use the feather library for Python


## Parameters


```python
# table type = tblType

all = "mentions", "eventsDatabase", "gdelt knowledge graph"
gkg = ["gdelt knowledge graph"]
events = "events" "database"
mentions =  "mentions database"

alls = ['gkg','events']
```

## Global variables


```python
gkgHeaders = pd.read_csv(
    '../utils/schema_csvs/GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.tsv',
    delimiter='\t',usecols=['tableId','dataType','Description']
    )
gkgHeaders.tableId.tolist();

eventsDbHeaders = pd.read_csv('../utils/schema_csvs/GDELT_2.0_Events_Column_Labels_Header_Row_Sep2016.csv',
                         delimiter=',',usecols=['tableId','dataType','Description'])
eventsDbHeaders.tableId.tolist();

mentionsHeaders = pd.read_csv('../utils/schema_csvs/GDELT_2.0_eventMentions_Column_Labels_Header_Row_Sep2016.tsv',
                         delimiter='\t',usecols=['tableId','dataType','Description'])
mentionsHeaders.tableId.tolist();


```


```python
strings = ['http://data.gdeltproject.org/gdeltv2/20150225234500.gkg.csv.zip',
          'http://data.gdeltproject.org/gdeltv2/20160919070000.mentions.CSV.zip',
          'http://data.gdeltproject.org/gdeltv2/20160919070000.export.CSV.zip']

dbType = re.search(
            '(mentions|export|gkg)',
            strings[2]
        ).group()
dbType
```




    'export'



## Code Pieces and Functions


```python
defaultDateEntry = ""
stringDateEntry = " 2016 09 18"
historicalDateEntry = "2015 02 25"
errorDate = "What in the heck"
```


```python
date = defaultDateEntry
time = ""
```

# Date Functionality (Date ranges)

Use the numpy date range functionality to create strings of dates between ranges in a list.  Then, use the dateutil tool to parse those strings into the correct format.  Then run a query for each date, return the dataframe, and concatenate into a single one.  


```python
import numpy as np
np.arange('2016-08-01', '2016-09-16', dtype='datetime64[D]')
```




    array(['2016-08-01', '2016-08-02', '2016-08-03', '2016-08-04',
           '2016-08-05', '2016-08-06', '2016-08-07', '2016-08-08',
           '2016-08-09', '2016-08-10', '2016-08-11', '2016-08-12',
           '2016-08-13', '2016-08-14', '2016-08-15', '2016-08-16',
           '2016-08-17', '2016-08-18', '2016-08-19', '2016-08-20',
           '2016-08-21', '2016-08-22', '2016-08-23', '2016-08-24',
           '2016-08-25', '2016-08-26', '2016-08-27', '2016-08-28',
           '2016-08-29', '2016-08-30', '2016-08-31', '2016-09-01',
           '2016-09-02', '2016-09-03', '2016-09-04', '2016-09-05',
           '2016-09-06', '2016-09-07', '2016-09-08', '2016-09-09',
           '2016-09-10', '2016-09-11', '2016-09-12', '2016-09-13',
           '2016-09-14', '2016-09-15'], dtype='datetime64[D]')



### Pulling Date information


```python
#############################################
# Parse the date
#############################################


from dateutil.parser import parse
import pandas as pd
import numpy as np 
import requests
import datetime



def parse_date(var):
    """Return datetime object from string."""
    
    try:
        return np.where(isinstance(parse(var),datetime.datetime),
                 parse(var),"Error")             
    except:
        return "You entered an incorrect date.  Check your date format."

    
def dateInputCheck(parse_DateVar):
    """Check user input to retrieve date query."""
    
    return np.where(len(parse_DateVar)==0,datetime.datetime.now(),
             parse_date(parse_DateVar)) 


def gdelt_timeString(dateInputVar):
    """Convert date to GDELT string file format for query."""
    
    multiplier = dateInputVar.tolist().minute / 15
    multiple = 15 * multiplier
    queryDate = np.where(
            multiplier > 1,dateInputVar.tolist().replace(
            minute=0, second=0) + datetime.timedelta(
            minutes=multiple),
            dateInputVar.tolist().replace(
            minute=0, second=0,microsecond=0000)
            )
    
    # Check for date equality on historical query
    modifierTip = datetime.datetime.now().replace(
        hour=0,minute=0,second=0,microsecond=0
        ) == queryDate.tolist().replace(
        hour=0,minute=0,second=0,microsecond=0
        )
    
    # Based on modifier, get oldest file for historical query
    queryDate = np.where(
        modifierTip==False,
        queryDate.tolist().replace(
            hour=23,
            minute=45,
            second=00,
            microsecond=0000
            ),queryDate
        )
    
#     print modifierTip
    return queryDate.tolist().strftime("%Y%m%d%H%M%S")

#############################################
# Match parsed date to GDELT master list
#############################################

def match_date(dateString):
    """Return dataframe with GDELT data for matching date"""
    
    masterListUrl = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
    directory = requests.get(masterListUrl)
    results = directory.content.split('\n')
    results = map(lambda x: x.split(' '),results)
    masterListdf = pd.DataFrame(results)
    return masterListdf[
        masterListdf[2].str.contains(
            dateString
            )==True
        ]
    

```


```python
results = match_date(gdelt_timeString(dateInputCheck(date)))
```


```python
results
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>166641</th>
      <td>174299</td>
      <td>39ba2ff2f6324fc991c4e1a108156539</td>
      <td>http://data.gdeltproject.org/gdeltv2/201609212...</td>
    </tr>
    <tr>
      <th>166642</th>
      <td>439023</td>
      <td>2f07528e827198da2ef4d4edff1eb098</td>
      <td>http://data.gdeltproject.org/gdeltv2/201609212...</td>
    </tr>
    <tr>
      <th>166643</th>
      <td>16871119</td>
      <td>2e923aa27d18fed741e9b03b4c5b2d2b</td>
      <td>http://data.gdeltproject.org/gdeltv2/201609212...</td>
    </tr>
  </tbody>
</table>
</div>



## Munging Data: Extracting Specific Datasets or all of them

Work with the returned GDELT dataframe.  Specific whether we are pulling the `mentions`, `events`, or `gkg` date for the day or all.  


```python
zippie2 = results.reset_index().ix[1][2]
```


```python
#############################################
# GDELT data download and extraction
#############################################

from StringIO import StringIO
import pandas as pd
import requests
import zipfile
import re

def downloadAndExtract(gdeltUrl):
    """Downloads and extracts GDELT zips without saving to disk"""
    
    response = requests.get(gdeltUrl, stream=True)
    zipdata = StringIO()
    zipdata.write(response.content)
    gdelt_zipfile = zipfile.ZipFile(zipdata,'r')
    name = re.search('(([\d]{4,}).*)',gdelt_zipfile.namelist()[0]).group().replace('.zip',"")
    data = gdelt_zipfile.read(name)
    gdelt_zipfile.close()
    del zipdata,gdelt_zipfile,name,response
    return pd.read_csv(StringIO(data),delimiter='\t',header=None)
    

def add_header(gdeltUrl):
    """Returns the header rows for the dataframe"""
    
    dbType = re.search(
        '(mentions|export|gkg)',
        gdeltUrl
        ).group()
    
    if dbType == "gkg":
        headers = gkgHeaders.tableId.tolist()
    
    elif dbType == "mentions":
        headers = mentionsHeaders.tableId.tolist()
        
    elif dbType == "export":
        headers = eventsDbHeaders.tableId.tolist()
        
    return headers
```


```python
zippie2
```




    'http://data.gdeltproject.org/gdeltv2/20160921230000.mentions.CSV.zip'




```python
gdelt_df = downloadAndExtract(zippie)
gdelt_df.columns = add_header(zippie)
```


```python
gdelt_df2 = downloadAndExtract(zippie2)
gdelt_df2.columns = add_header(zippie2)
```


```python
combined = gdelt_df.merge(gdelt_df2,how='right',on='GLOBALEVENTID')
```


```python
combined.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 11767 entries, 0 to 11766
    Data columns (total 76 columns):
    GLOBALEVENTID                11767 non-null float64
    SQLDATE                      2785 non-null float64
    MonthYear                    2785 non-null float64
    Year                         2785 non-null float64
    FractionDate                 2785 non-null float64
    Actor1Code                   2550 non-null object
    Actor1Name                   2550 non-null object
    Actor1CountryCode            1573 non-null object
    Actor1KnownGroupCode         63 non-null object
    Actor1EthnicCode             31 non-null object
    Actor1Religion1Code          55 non-null object
    Actor1Religion2Code          13 non-null object
    Actor1Type1Code              1220 non-null object
    Actor1Type2Code              68 non-null object
    Actor1Type3Code              0 non-null float64
    Actor2Code                   2005 non-null object
    Actor2Name                   2005 non-null object
    Actor2CountryCode            1246 non-null object
    Actor2KnownGroupCode         40 non-null object
    Actor2EthnicCode             18 non-null object
    Actor2Religion1Code          43 non-null object
    Actor2Religion2Code          12 non-null object
    Actor2Type1Code              931 non-null object
    Actor2Type2Code              67 non-null object
    Actor2Type3Code              1 non-null object
    IsRootEvent                  2785 non-null float64
    EventCode                    2785 non-null float64
    EventBaseCode                2785 non-null float64
    EventRootCode                2785 non-null float64
    QuadClass                    2785 non-null float64
    GoldsteinScale               2785 non-null float64
    NumMentions                  2785 non-null float64
    NumSources                   2785 non-null float64
    NumArticles                  2785 non-null float64
    AvgTone                      2785 non-null float64
    Actor1Geo_Type               2785 non-null float64
    Actor1Geo_FullName           2502 non-null object
    Actor1Geo_CountryCode        2502 non-null object
    Actor1Geo_ADM1Code           2502 non-null object
    Actor1Geo_ADM2Code           1349 non-null object
    Actor1Geo_Lat                2502 non-null float64
    Actor1Geo_Long               2502 non-null float64
    Actor1Geo_FeatureID          2502 non-null object
    Actor2Geo_Type               2785 non-null float64
    Actor2Geo_FullName           1965 non-null object
    Actor2Geo_CountryCode        1965 non-null object
    Actor2Geo_ADM1Code           1965 non-null object
    Actor2Geo_ADM2Code           858 non-null object
    Actor2Geo_Lat                1965 non-null float64
    Actor2Geo_Long               1965 non-null float64
    Actor2Geo_FeatureID          1965 non-null object
    ActionGeo_Type               2785 non-null float64
    ActionGeo_FullName           2734 non-null object
    ActionGeo_CountryCode        2734 non-null object
    ActionGeo_ADM1Code           2734 non-null object
    ActionGeo_ADM2Code           1207 non-null object
    ActionGeo_Lat                2734 non-null float64
    ActionGeo_Long               2734 non-null float64
    ActionGeo_FeatureID          2734 non-null object
    DATEADDED                    2785 non-null float64
    SOURCEURL                    2785 non-null object
    EventTimeDate                11767 non-null int64
    MentionTimeDate              11767 non-null int64
    MentionType                  11767 non-null int64
    MentionSourceName            11767 non-null object
    MentionIdentifier            11767 non-null object
    SentenceID                   11767 non-null int64
    Actor1CharOffset             11767 non-null int64
    Actor2CharOffset             11767 non-null int64
    ActionCharOffset             11767 non-null int64
    InRawText                    11767 non-null int64
    Confidence                   11767 non-null int64
    MentionDocLen                11767 non-null int64
    MentionDocTone               11767 non-null float64
    MentionDocTranslationInfo    0 non-null float64
    Extras                       0 non-null float64
    dtypes: float64(29), int64(10), object(37)
    memory usage: 6.9+ MB



```python
combined.tail()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>GLOBALEVENTID</th>
      <th>SQLDATE</th>
      <th>MonthYear</th>
      <th>Year</th>
      <th>FractionDate</th>
      <th>Actor1Code</th>
      <th>Actor1Name</th>
      <th>Actor1CountryCode</th>
      <th>Actor1KnownGroupCode</th>
      <th>Actor1EthnicCode</th>
      <th>...</th>
      <th>SentenceID</th>
      <th>Actor1CharOffset</th>
      <th>Actor2CharOffset</th>
      <th>ActionCharOffset</th>
      <th>InRawText</th>
      <th>Confidence</th>
      <th>MentionDocLen</th>
      <th>MentionDocTone</th>
      <th>MentionDocTranslationInfo</th>
      <th>Extras</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>11762</th>
      <td>581379923.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>4</td>
      <td>879</td>
      <td>929</td>
      <td>901</td>
      <td>1</td>
      <td>100</td>
      <td>1547</td>
      <td>0.000000</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11763</th>
      <td>581387463.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1</td>
      <td>499</td>
      <td>477</td>
      <td>521</td>
      <td>1</td>
      <td>100</td>
      <td>1547</td>
      <td>0.000000</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11764</th>
      <td>581408219.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>2</td>
      <td>687</td>
      <td>630</td>
      <td>665</td>
      <td>1</td>
      <td>20</td>
      <td>813</td>
      <td>-9.929078</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11765</th>
      <td>581408220.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>2</td>
      <td>704</td>
      <td>617</td>
      <td>682</td>
      <td>0</td>
      <td>20</td>
      <td>813</td>
      <td>-9.929078</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>11766</th>
      <td>581408221.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>2</td>
      <td>683</td>
      <td>596</td>
      <td>661</td>
      <td>0</td>
      <td>20</td>
      <td>813</td>
      <td>-9.929078</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 76 columns</p>
</div>




```python
# combined.[(combined.Confidence != None) & (combined.MonthYear != None)]
combined.fillna('')[combined.GoldsteinScale <= -5.2]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>GLOBALEVENTID</th>
      <th>SQLDATE</th>
      <th>MonthYear</th>
      <th>Year</th>
      <th>FractionDate</th>
      <th>Actor1Code</th>
      <th>Actor1Name</th>
      <th>Actor1CountryCode</th>
      <th>Actor1KnownGroupCode</th>
      <th>Actor1EthnicCode</th>
      <th>...</th>
      <th>SentenceID</th>
      <th>Actor1CharOffset</th>
      <th>Actor2CharOffset</th>
      <th>ActionCharOffset</th>
      <th>InRawText</th>
      <th>Confidence</th>
      <th>MentionDocLen</th>
      <th>MentionDocTone</th>
      <th>MentionDocTranslationInfo</th>
      <th>Extras</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>36</th>
      <td>581409211.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7</td>
      <td>LBNGOV</td>
      <td>TYRE</td>
      <td>LBN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>1600</td>
      <td>1641</td>
      <td>1661</td>
      <td>0</td>
      <td>10</td>
      <td>3229</td>
      <td>-4.060914</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>37</th>
      <td>581409212.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7</td>
      <td>LBNGOV</td>
      <td>TYRE</td>
      <td>LBN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>1600</td>
      <td>1636</td>
      <td>1647</td>
      <td>1</td>
      <td>30</td>
      <td>3229</td>
      <td>-4.060914</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>46</th>
      <td>581409221.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.7</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>1600</td>
      <td>-1</td>
      <td>1694</td>
      <td>0</td>
      <td>10</td>
      <td>3229</td>
      <td>-4.060914</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>55</th>
      <td>581409230.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.71</td>
      <td>LBN</td>
      <td>TYRE</td>
      <td>LBN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>842</td>
      <td>791</td>
      <td>829</td>
      <td>1</td>
      <td>60</td>
      <td>2749</td>
      <td>-7.922912</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>56</th>
      <td>581409231.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.71</td>
      <td>LBN</td>
      <td>TYRE</td>
      <td>LBN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>842</td>
      <td>854</td>
      <td>829</td>
      <td>0</td>
      <td>40</td>
      <td>2749</td>
      <td>-7.922912</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>67</th>
      <td>581409242.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.71</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>192</td>
      <td>499</td>
      <td>342</td>
      <td>0</td>
      <td>20</td>
      <td>1777</td>
      <td>-9.003215</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>81</th>
      <td>581409255.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>-1</td>
      <td>1943</td>
      <td>2012</td>
      <td>1</td>
      <td>100</td>
      <td>2229</td>
      <td>-3.140097</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>111</th>
      <td>581409284.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>29</td>
      <td>39</td>
      <td>1</td>
      <td>50</td>
      <td>3242</td>
      <td>-4.504505</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>137</th>
      <td>581409305.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>-1</td>
      <td>3980</td>
      <td>4010</td>
      <td>0</td>
      <td>20</td>
      <td>7521</td>
      <td>-0.867508</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>138</th>
      <td>581409305.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>9</td>
      <td>-1</td>
      <td>3719</td>
      <td>3741</td>
      <td>1</td>
      <td>100</td>
      <td>6763</td>
      <td>-1.218451</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>151</th>
      <td>581409318.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>-1</td>
      <td>1192</td>
      <td>1236</td>
      <td>1</td>
      <td>30</td>
      <td>3229</td>
      <td>-4.060914</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>152</th>
      <td>581409319.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>126</td>
      <td>192</td>
      <td>1</td>
      <td>10</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>159</th>
      <td>581409326.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>59</td>
      <td>8</td>
      <td>1</td>
      <td>30</td>
      <td>2405</td>
      <td>-1.913876</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>160</th>
      <td>581409327.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>59</td>
      <td>8</td>
      <td>0</td>
      <td>20</td>
      <td>2405</td>
      <td>-1.913876</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>206</th>
      <td>581409366.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>-1</td>
      <td>471</td>
      <td>550</td>
      <td>0</td>
      <td>30</td>
      <td>2685</td>
      <td>-6.060606</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>207</th>
      <td>581409367.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>-1</td>
      <td>471</td>
      <td>566</td>
      <td>1</td>
      <td>60</td>
      <td>2685</td>
      <td>-6.060606</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>231</th>
      <td>581409386.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>-1</td>
      <td>388</td>
      <td>369</td>
      <td>1</td>
      <td>100</td>
      <td>3571</td>
      <td>-6.260297</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>232</th>
      <td>581409387.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>-1</td>
      <td>388</td>
      <td>403</td>
      <td>1</td>
      <td>100</td>
      <td>3571</td>
      <td>-6.260297</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>234</th>
      <td>581409389.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>-1</td>
      <td>1819</td>
      <td>1805</td>
      <td>1</td>
      <td>100</td>
      <td>2947</td>
      <td>6.108202</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>279</th>
      <td>581409427.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>-1</td>
      <td>567</td>
      <td>391</td>
      <td>1</td>
      <td>30</td>
      <td>5801</td>
      <td>-2.300110</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>281</th>
      <td>581409429.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>-1</td>
      <td>1547</td>
      <td>1596</td>
      <td>1</td>
      <td>100</td>
      <td>3722</td>
      <td>-1.712329</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>282</th>
      <td>581409430.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>401</td>
      <td>419</td>
      <td>0</td>
      <td>40</td>
      <td>1270</td>
      <td>-11.872146</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>283</th>
      <td>581409431.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>77</td>
      <td>256</td>
      <td>0</td>
      <td>60</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>284</th>
      <td>581409432.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>28</td>
      <td>-1</td>
      <td>7204</td>
      <td>7222</td>
      <td>0</td>
      <td>30</td>
      <td>7190</td>
      <td>-6.610169</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>285</th>
      <td>581409433.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>27</td>
      <td>-1</td>
      <td>10011</td>
      <td>10165</td>
      <td>0</td>
      <td>10</td>
      <td>11927</td>
      <td>1.317790</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>290</th>
      <td>581409438.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>-1</td>
      <td>128</td>
      <td>240</td>
      <td>1</td>
      <td>30</td>
      <td>10235</td>
      <td>-2.095460</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>291</th>
      <td>581409439.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>178</td>
      <td>256</td>
      <td>0</td>
      <td>20</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>297</th>
      <td>581409445.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>-1</td>
      <td>2749</td>
      <td>2763</td>
      <td>0</td>
      <td>30</td>
      <td>5372</td>
      <td>-4.966887</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>299</th>
      <td>581409447.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>-1</td>
      <td>1159</td>
      <td>1172</td>
      <td>0</td>
      <td>30</td>
      <td>1435</td>
      <td>-8.433735</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>365</th>
      <td>581409500.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>AUS</td>
      <td>AUSTRALIA</td>
      <td>AUS</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>240</td>
      <td>350</td>
      <td>306</td>
      <td>0</td>
      <td>40</td>
      <td>2152</td>
      <td>-0.787402</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>392</th>
      <td>581409524.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BRA</td>
      <td>BRAZIL</td>
      <td>BRA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2231</td>
      <td>2208</td>
      <td>2322</td>
      <td>1</td>
      <td>50</td>
      <td>3140</td>
      <td>-7.952286</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>448</th>
      <td>581409576.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>BANK</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>20</td>
      <td>6936</td>
      <td>-1</td>
      <td>6980</td>
      <td>1</td>
      <td>60</td>
      <td>12032</td>
      <td>-2.600996</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>449</th>
      <td>581409577.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>BANK</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>20</td>
      <td>6936</td>
      <td>-1</td>
      <td>6980</td>
      <td>0</td>
      <td>40</td>
      <td>12032</td>
      <td>-2.600996</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>452</th>
      <td>581409580.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>COMPANIES</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>992</td>
      <td>-1</td>
      <td>1032</td>
      <td>1</td>
      <td>100</td>
      <td>3203</td>
      <td>-1.792829</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>458</th>
      <td>581409586.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>AIRLINE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>68</td>
      <td>106</td>
      <td>87</td>
      <td>1</td>
      <td>100</td>
      <td>2967</td>
      <td>0.795229</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>478</th>
      <td>581409602.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>COMPANIES</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2823</td>
      <td>2694</td>
      <td>2833</td>
      <td>1</td>
      <td>80</td>
      <td>3191</td>
      <td>-2.994012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>505</th>
      <td>581409628.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>BUS</td>
      <td>COMPANIES</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2843</td>
      <td>2700</td>
      <td>2847</td>
      <td>0</td>
      <td>20</td>
      <td>3191</td>
      <td>-2.994012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>524</th>
      <td>581409645.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2103</td>
      <td>-1</td>
      <td>2139</td>
      <td>1</td>
      <td>100</td>
      <td>3290</td>
      <td>-4.419890</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>525</th>
      <td>581409646.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2094</td>
      <td>-1</td>
      <td>2130</td>
      <td>0</td>
      <td>10</td>
      <td>3290</td>
      <td>-4.419890</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>526</th>
      <td>581409647.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>2653</td>
      <td>2677</td>
      <td>2660</td>
      <td>0</td>
      <td>40</td>
      <td>6742</td>
      <td>1.115880</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>527</th>
      <td>581409648.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>2552</td>
      <td>2576</td>
      <td>2559</td>
      <td>0</td>
      <td>20</td>
      <td>5668</td>
      <td>1.368421</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>529</th>
      <td>581409650.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1773</td>
      <td>1815</td>
      <td>1866</td>
      <td>0</td>
      <td>40</td>
      <td>2452</td>
      <td>6.913580</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>537</th>
      <td>581409658.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>2425</td>
      <td>2460</td>
      <td>2432</td>
      <td>0</td>
      <td>20</td>
      <td>5329</td>
      <td>1.325178</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>539</th>
      <td>581409660.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>14</td>
      <td>2975</td>
      <td>2987</td>
      <td>2982</td>
      <td>0</td>
      <td>10</td>
      <td>5372</td>
      <td>-4.966887</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>540</th>
      <td>581409661.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CAN</td>
      <td>CANADA</td>
      <td>CAN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>14</td>
      <td>2993</td>
      <td>3021</td>
      <td>3000</td>
      <td>0</td>
      <td>10</td>
      <td>5372</td>
      <td>-4.966887</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>554</th>
      <td>581409675.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CHN</td>
      <td>CHINA</td>
      <td>CHN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>522</td>
      <td>546</td>
      <td>528</td>
      <td>1</td>
      <td>80</td>
      <td>686</td>
      <td>3.252033</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>555</th>
      <td>581409676.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CHN</td>
      <td>CHINA</td>
      <td>CHN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>522</td>
      <td>546</td>
      <td>528</td>
      <td>0</td>
      <td>20</td>
      <td>686</td>
      <td>3.252033</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>572</th>
      <td>581409693.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CHRCTH</td>
      <td>CATHOLIC</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>759</td>
      <td>-1</td>
      <td>798</td>
      <td>0</td>
      <td>10</td>
      <td>6114</td>
      <td>-4.872881</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>573</th>
      <td>581409694.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CHRCTH</td>
      <td>CATHOLIC</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>759</td>
      <td>-1</td>
      <td>798</td>
      <td>0</td>
      <td>10</td>
      <td>6114</td>
      <td>-4.872881</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>584</th>
      <td>581409703.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COG</td>
      <td>CONGO</td>
      <td>COG</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>-1</td>
      <td>17</td>
      <td>1</td>
      <td>100</td>
      <td>2567</td>
      <td>-14.492754</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>585</th>
      <td>581409703.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COG</td>
      <td>CONGO</td>
      <td>COG</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>-1</td>
      <td>17</td>
      <td>1</td>
      <td>100</td>
      <td>2672</td>
      <td>-14.251208</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>608</th>
      <td>581409723.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>2631</td>
      <td>-1</td>
      <td>2591</td>
      <td>1</td>
      <td>20</td>
      <td>5249</td>
      <td>-7.407407</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>609</th>
      <td>581409724.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1823</td>
      <td>-1</td>
      <td>1877</td>
      <td>1</td>
      <td>60</td>
      <td>2452</td>
      <td>6.913580</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>610</th>
      <td>581409725.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>342</td>
      <td>-1</td>
      <td>424</td>
      <td>1</td>
      <td>100</td>
      <td>2710</td>
      <td>-3.794643</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>615</th>
      <td>581409730.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>SECURITY FORCE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>15</td>
      <td>4507</td>
      <td>-1</td>
      <td>4523</td>
      <td>1</td>
      <td>100</td>
      <td>10652</td>
      <td>-4.256804</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>616</th>
      <td>581409731.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>315</td>
      <td>-1</td>
      <td>363</td>
      <td>1</td>
      <td>100</td>
      <td>608</td>
      <td>-10.714286</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>617</th>
      <td>581409732.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>306</td>
      <td>-1</td>
      <td>315</td>
      <td>1</td>
      <td>100</td>
      <td>1806</td>
      <td>-3.594771</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>619</th>
      <td>581409734.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2358</td>
      <td>2378</td>
      <td>2365</td>
      <td>1</td>
      <td>100</td>
      <td>2964</td>
      <td>-3.821656</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>627</th>
      <td>581409742.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>304</td>
      <td>313</td>
      <td>322</td>
      <td>1</td>
      <td>50</td>
      <td>2710</td>
      <td>-3.794643</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>640</th>
      <td>581409753.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>159</td>
      <td>64</td>
      <td>80</td>
      <td>1</td>
      <td>50</td>
      <td>548</td>
      <td>-7.692308</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>641</th>
      <td>581409754.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>484</td>
      <td>442</td>
      <td>460</td>
      <td>1</td>
      <td>100</td>
      <td>2518</td>
      <td>-7.226107</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>647</th>
      <td>581409760.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>SECURITY FORCE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>14</td>
      <td>4403</td>
      <td>4388</td>
      <td>4340</td>
      <td>0</td>
      <td>10</td>
      <td>10652</td>
      <td>-4.256804</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>649</th>
      <td>581409762.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>SECURITY FORCE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>1235</td>
      <td>1089</td>
      <td>1216</td>
      <td>1</td>
      <td>50</td>
      <td>3736</td>
      <td>-0.860585</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>670</th>
      <td>581409780.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>-1</td>
      <td>-1</td>
      <td>-1</td>
      <td>0</td>
      <td>10</td>
      <td>1864</td>
      <td>-4.666667</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>671</th>
      <td>581409780.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1083</td>
      <td>980</td>
      <td>1070</td>
      <td>1</td>
      <td>100</td>
      <td>2730</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>672</th>
      <td>581409781.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE OFFICER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>412</td>
      <td>367</td>
      <td>400</td>
      <td>0</td>
      <td>20</td>
      <td>1273</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>673</th>
      <td>581409782.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE OFFICER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>181</td>
      <td>45</td>
      <td>162</td>
      <td>0</td>
      <td>20</td>
      <td>594</td>
      <td>-7.547170</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>674</th>
      <td>581409783.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>510</td>
      <td>440</td>
      <td>498</td>
      <td>0</td>
      <td>20</td>
      <td>3015</td>
      <td>-3.543307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>675</th>
      <td>581409784.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>531</td>
      <td>461</td>
      <td>519</td>
      <td>0</td>
      <td>20</td>
      <td>3015</td>
      <td>-3.543307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>676</th>
      <td>581409785.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE OFFICER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2687</td>
      <td>2616</td>
      <td>2662</td>
      <td>1</td>
      <td>70</td>
      <td>9235</td>
      <td>-3.241491</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>677</th>
      <td>581409786.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE OFFICER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>412</td>
      <td>367</td>
      <td>391</td>
      <td>0</td>
      <td>20</td>
      <td>1273</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>678</th>
      <td>581409787.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>143</td>
      <td>162</td>
      <td>150</td>
      <td>1</td>
      <td>100</td>
      <td>4250</td>
      <td>-4.526749</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>679</th>
      <td>581409788.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>POLICE OFFICER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>-1</td>
      <td>2667</td>
      <td>2714</td>
      <td>0</td>
      <td>10</td>
      <td>9235</td>
      <td>-3.241491</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>681</th>
      <td>581409790.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>COP</td>
      <td>DEPUTY</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1217</td>
      <td>1182</td>
      <td>1195</td>
      <td>0</td>
      <td>10</td>
      <td>1435</td>
      <td>-8.433735</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>700</th>
      <td>581409809.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CRM</td>
      <td>CRIMINAL</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>1787</td>
      <td>1960</td>
      <td>1928</td>
      <td>0</td>
      <td>10</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>744</th>
      <td>581409851.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CVL</td>
      <td>VILLAGE</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2818</td>
      <td>-1</td>
      <td>2749</td>
      <td>1</td>
      <td>30</td>
      <td>3971</td>
      <td>-1.401051</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>745</th>
      <td>581409852.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CVL</td>
      <td>COMMUNITY</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>29</td>
      <td>-1</td>
      <td>39</td>
      <td>1</td>
      <td>50</td>
      <td>3242</td>
      <td>-4.504505</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>765</th>
      <td>581409872.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>CVL</td>
      <td>NEIGHBORHOOD</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>418</td>
      <td>261</td>
      <td>349</td>
      <td>1</td>
      <td>100</td>
      <td>1155</td>
      <td>-7.619048</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>816</th>
      <td>581409920.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>SCHOOL</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2058</td>
      <td>-1</td>
      <td>2027</td>
      <td>1</td>
      <td>100</td>
      <td>3579</td>
      <td>-4.232804</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>818</th>
      <td>581409922.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>STUDENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>8</td>
      <td>-1</td>
      <td>34</td>
      <td>1</td>
      <td>100</td>
      <td>883</td>
      <td>-3.311258</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>819</th>
      <td>581409923.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>STUDENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>59</td>
      <td>-1</td>
      <td>85</td>
      <td>1</td>
      <td>100</td>
      <td>883</td>
      <td>-3.311258</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>826</th>
      <td>581409930.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>UNIVERSITY</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>132</td>
      <td>236</td>
      <td>270</td>
      <td>1</td>
      <td>100</td>
      <td>3579</td>
      <td>-4.232804</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>861</th>
      <td>581409965.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>STUDENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1062</td>
      <td>1132</td>
      <td>1071</td>
      <td>0</td>
      <td>20</td>
      <td>2744</td>
      <td>-4.291845</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>862</th>
      <td>581409966.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>STUDENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>700</td>
      <td>737</td>
      <td>709</td>
      <td>1</td>
      <td>100</td>
      <td>955</td>
      <td>-6.666667</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>863</th>
      <td>581409967.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDU</td>
      <td>STUDENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>1877</td>
      <td>1937</td>
      <td>1886</td>
      <td>0</td>
      <td>20</td>
      <td>11363</td>
      <td>-6.850054</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>865</th>
      <td>581409969.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>EDUEDU</td>
      <td>SCHOOL</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>132</td>
      <td>277</td>
      <td>262</td>
      <td>1</td>
      <td>100</td>
      <td>883</td>
      <td>-3.311258</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>886</th>
      <td>581409983.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>ESP</td>
      <td>BARCELONA</td>
      <td>ESP</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>86</td>
      <td>-1</td>
      <td>153</td>
      <td>1</td>
      <td>50</td>
      <td>3232</td>
      <td>-4.609929</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>887</th>
      <td>581409984.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>ESP</td>
      <td>BARCELONA</td>
      <td>ESP</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>0</td>
      <td>-1</td>
      <td>67</td>
      <td>1</td>
      <td>70</td>
      <td>3232</td>
      <td>-4.609929</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>974</th>
      <td>581410049.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GBR</td>
      <td>BRITAIN</td>
      <td>GBR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>2293</td>
      <td>2430</td>
      <td>2504</td>
      <td>0</td>
      <td>20</td>
      <td>5595</td>
      <td>-6.992231</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1030</th>
      <td>581410104.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>FIREFIGHTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2208</td>
      <td>2231</td>
      <td>2322</td>
      <td>1</td>
      <td>50</td>
      <td>3140</td>
      <td>-7.952286</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1038</th>
      <td>581410112.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>KING</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>172</td>
      <td>97</td>
      <td>123</td>
      <td>1</td>
      <td>100</td>
      <td>331</td>
      <td>-4.761905</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1039</th>
      <td>581410113.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>GOVERNMENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>596</td>
      <td>654</td>
      <td>553</td>
      <td>1</td>
      <td>60</td>
      <td>1190</td>
      <td>-0.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1056</th>
      <td>581410130.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>PRIME MINISTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2860</td>
      <td>2926</td>
      <td>2931</td>
      <td>0</td>
      <td>20</td>
      <td>3843</td>
      <td>0.975610</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1057</th>
      <td>581410131.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>PRIME MINISTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2860</td>
      <td>2926</td>
      <td>2931</td>
      <td>1</td>
      <td>40</td>
      <td>3843</td>
      <td>0.975610</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1065</th>
      <td>581410138.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>DESPOT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>97</td>
      <td>221</td>
      <td>203</td>
      <td>1</td>
      <td>30</td>
      <td>5722</td>
      <td>-2.558854</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1066</th>
      <td>581410139.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>DESPOT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>97</td>
      <td>227</td>
      <td>209</td>
      <td>0</td>
      <td>20</td>
      <td>5722</td>
      <td>-2.558854</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1090</th>
      <td>581410163.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>GOVERNMENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>964</td>
      <td>931</td>
      <td>938</td>
      <td>0</td>
      <td>20</td>
      <td>1714</td>
      <td>-6.756757</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1098</th>
      <td>581410171.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>INTERIOR MINIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>817</td>
      <td>866</td>
      <td>835</td>
      <td>1</td>
      <td>100</td>
      <td>1192</td>
      <td>-8.490566</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1118</th>
      <td>581410188.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOV</td>
      <td>MINIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>18</td>
      <td>3593</td>
      <td>3637</td>
      <td>3603</td>
      <td>1</td>
      <td>100</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1131</th>
      <td>581410200.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>GOVHLH</td>
      <td>HEALTH DEPARTMENT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>126</td>
      <td>-1</td>
      <td>192</td>
      <td>1</td>
      <td>10</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2050</th>
      <td>581411023.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>SYRMIL</td>
      <td>SYRIA</td>
      <td>SYR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>1833</td>
      <td>1899</td>
      <td>1890</td>
      <td>0</td>
      <td>20</td>
      <td>3290</td>
      <td>-4.419890</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2057</th>
      <td>581411030.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUN</td>
      <td>TUNISIA</td>
      <td>TUN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>17</td>
      <td>-1</td>
      <td>5</td>
      <td>0</td>
      <td>20</td>
      <td>9566</td>
      <td>-4.032766</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2058</th>
      <td>581411031.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUN</td>
      <td>TUNISIA</td>
      <td>TUN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>17</td>
      <td>-1</td>
      <td>5</td>
      <td>1</td>
      <td>80</td>
      <td>9566</td>
      <td>-4.032766</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2059</th>
      <td>581411032.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUN</td>
      <td>TUNISIA</td>
      <td>TUN</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>829</td>
      <td>934</td>
      <td>787</td>
      <td>1</td>
      <td>100</td>
      <td>9566</td>
      <td>-4.032766</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2061</th>
      <td>581411034.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUR</td>
      <td>TURKISH</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>480</td>
      <td>396</td>
      <td>429</td>
      <td>0</td>
      <td>10</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2062</th>
      <td>581411035.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUR</td>
      <td>ISTANBUL</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>19</td>
      <td>3036</td>
      <td>2983</td>
      <td>2996</td>
      <td>1</td>
      <td>80</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2063</th>
      <td>581411036.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUR</td>
      <td>ISTANBUL</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>19</td>
      <td>3067</td>
      <td>3010</td>
      <td>3020</td>
      <td>0</td>
      <td>20</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2066</th>
      <td>581411039.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUR</td>
      <td>TURKISH</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>1459</td>
      <td>1368</td>
      <td>1445</td>
      <td>0</td>
      <td>10</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2067</th>
      <td>581411040.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TUR</td>
      <td>TURKISH</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>1459</td>
      <td>1368</td>
      <td>1445</td>
      <td>0</td>
      <td>10</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2072</th>
      <td>581411045.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>TURCOP</td>
      <td>TURKISH</td>
      <td>TUR</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>1442</td>
      <td>1368</td>
      <td>1432</td>
      <td>1</td>
      <td>30</td>
      <td>3716</td>
      <td>-2.500000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2086</th>
      <td>581411059.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>TERRORIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>15</td>
      <td>3663</td>
      <td>3687</td>
      <td>3673</td>
      <td>0</td>
      <td>20</td>
      <td>3943</td>
      <td>-5.376344</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2087</th>
      <td>581411060.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>MILITANT</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>17</td>
      <td>4749</td>
      <td>4766</td>
      <td>4759</td>
      <td>1</td>
      <td>30</td>
      <td>10652</td>
      <td>-4.256804</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2088</th>
      <td>581411061.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>FIGHTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>1231</td>
      <td>1256</td>
      <td>1244</td>
      <td>1</td>
      <td>30</td>
      <td>4593</td>
      <td>-1.859230</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2089</th>
      <td>581411062.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>TERRORIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1990</td>
      <td>2014</td>
      <td>2000</td>
      <td>1</td>
      <td>100</td>
      <td>2272</td>
      <td>2.298851</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2090</th>
      <td>581411063.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>TERRORIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2166</td>
      <td>2190</td>
      <td>2176</td>
      <td>0</td>
      <td>20</td>
      <td>2413</td>
      <td>-4.116223</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2091</th>
      <td>581411064.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>TERRORIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2166</td>
      <td>2190</td>
      <td>2176</td>
      <td>0</td>
      <td>20</td>
      <td>2413</td>
      <td>-4.116223</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2092</th>
      <td>581411065.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>TERRORIST</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2166</td>
      <td>2190</td>
      <td>2176</td>
      <td>1</td>
      <td>60</td>
      <td>2413</td>
      <td>-4.116223</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2093</th>
      <td>581411066.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>FIGHTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>123</td>
      <td>163</td>
      <td>98</td>
      <td>0</td>
      <td>40</td>
      <td>4593</td>
      <td>-1.859230</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2094</th>
      <td>581411067.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>UAF</td>
      <td>FIGHTER</td>
      <td></td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>123</td>
      <td>163</td>
      <td>98</td>
      <td>0</td>
      <td>40</td>
      <td>4593</td>
      <td>-1.859230</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2265</th>
      <td>581411221.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>160</td>
      <td>-1</td>
      <td>209</td>
      <td>0</td>
      <td>10</td>
      <td>1273</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2266</th>
      <td>581411222.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>179</td>
      <td>-1</td>
      <td>241</td>
      <td>0</td>
      <td>30</td>
      <td>1273</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2267</th>
      <td>581411223.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>OHIO</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>173</td>
      <td>-1</td>
      <td>197</td>
      <td>1</td>
      <td>10</td>
      <td>1273</td>
      <td>-4.017857</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2268</th>
      <td>581411224.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>NEW YORK</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>3471</td>
      <td>-1</td>
      <td>3526</td>
      <td>0</td>
      <td>20</td>
      <td>9235</td>
      <td>-3.241491</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2269</th>
      <td>581411225.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>16</td>
      <td>3565</td>
      <td>-1</td>
      <td>3589</td>
      <td>0</td>
      <td>40</td>
      <td>4250</td>
      <td>-4.526749</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2270</th>
      <td>581411226.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>488</td>
      <td>-1</td>
      <td>502</td>
      <td>0</td>
      <td>40</td>
      <td>1481</td>
      <td>-12.015504</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2276</th>
      <td>581411232.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>95</td>
      <td>-1</td>
      <td>191</td>
      <td>0</td>
      <td>20</td>
      <td>2633</td>
      <td>-5.870445</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2277</th>
      <td>581411233.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>21</td>
      <td>5828</td>
      <td>-1</td>
      <td>5846</td>
      <td>0</td>
      <td>20</td>
      <td>6627</td>
      <td>-8.340728</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2278</th>
      <td>581411234.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>339</td>
      <td>-1</td>
      <td>427</td>
      <td>0</td>
      <td>40</td>
      <td>1481</td>
      <td>-12.015504</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2279</th>
      <td>581411235.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>68</td>
      <td>-1</td>
      <td>140</td>
      <td>0</td>
      <td>40</td>
      <td>1116</td>
      <td>-13.440860</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2280</th>
      <td>581411236.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>61</td>
      <td>-1</td>
      <td>206</td>
      <td>0</td>
      <td>40</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2281</th>
      <td>581411237.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>77</td>
      <td>-1</td>
      <td>256</td>
      <td>0</td>
      <td>10</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2282</th>
      <td>581411238.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>77</td>
      <td>-1</td>
      <td>256</td>
      <td>0</td>
      <td>10</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2283</th>
      <td>581411239.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>27</td>
      <td>10011</td>
      <td>-1</td>
      <td>10165</td>
      <td>0</td>
      <td>10</td>
      <td>11927</td>
      <td>1.317790</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2284</th>
      <td>581411240.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>452</td>
      <td>-1</td>
      <td>466</td>
      <td>0</td>
      <td>20</td>
      <td>2053</td>
      <td>-8.955224</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2285</th>
      <td>581411241.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>AMERICAN</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>75</td>
      <td>-1</td>
      <td>21</td>
      <td>1</td>
      <td>100</td>
      <td>483</td>
      <td>0.000000</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2288</th>
      <td>581411244.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>9</td>
      <td>2554</td>
      <td>2785</td>
      <td>2596</td>
      <td>0</td>
      <td>10</td>
      <td>5570</td>
      <td>-4.596413</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2289</th>
      <td>581411245.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>9</td>
      <td>2533</td>
      <td>2764</td>
      <td>2575</td>
      <td>0</td>
      <td>10</td>
      <td>5570</td>
      <td>-4.596413</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2350</th>
      <td>581411297.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ARKANSAS</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>586</td>
      <td>646</td>
      <td>653</td>
      <td>1</td>
      <td>100</td>
      <td>1687</td>
      <td>-4.332130</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2351</th>
      <td>581411298.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>440</td>
      <td>510</td>
      <td>498</td>
      <td>0</td>
      <td>20</td>
      <td>3015</td>
      <td>-3.543307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2352</th>
      <td>581411299.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>461</td>
      <td>531</td>
      <td>519</td>
      <td>0</td>
      <td>20</td>
      <td>3015</td>
      <td>-3.543307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2353</th>
      <td>581411300.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>1799</td>
      <td>1899</td>
      <td>1891</td>
      <td>0</td>
      <td>10</td>
      <td>3229</td>
      <td>-4.060914</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2359</th>
      <td>581411306.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>5</td>
      <td>1976</td>
      <td>2065</td>
      <td>1992</td>
      <td>0</td>
      <td>20</td>
      <td>3323</td>
      <td>1.711027</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2364</th>
      <td>581411311.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>1055</td>
      <td>-1</td>
      <td>1162</td>
      <td>0</td>
      <td>20</td>
      <td>1368</td>
      <td>-0.429185</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2365</th>
      <td>581411312.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>1070</td>
      <td>-1</td>
      <td>1177</td>
      <td>0</td>
      <td>20</td>
      <td>1368</td>
      <td>-0.429185</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2366</th>
      <td>581411313.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>TEXAS</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>1097</td>
      <td>1208</td>
      <td>1115</td>
      <td>1</td>
      <td>60</td>
      <td>1368</td>
      <td>-0.429185</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2381</th>
      <td>581411325.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ORLANDO</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2358</td>
      <td>2426</td>
      <td>2405</td>
      <td>0</td>
      <td>20</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2382</th>
      <td>581411326.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ORLANDO</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2301</td>
      <td>2368</td>
      <td>2349</td>
      <td>1</td>
      <td>60</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2383</th>
      <td>581411327.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ORLANDO</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2343</td>
      <td>2411</td>
      <td>2390</td>
      <td>0</td>
      <td>20</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2384</th>
      <td>581411328.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>NEW YORK</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2220</td>
      <td>2368</td>
      <td>2337</td>
      <td>1</td>
      <td>80</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2385</th>
      <td>581411329.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2195</td>
      <td>2411</td>
      <td>2381</td>
      <td>0</td>
      <td>20</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2386</th>
      <td>581411330.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2210</td>
      <td>2426</td>
      <td>2303</td>
      <td>0</td>
      <td>20</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2387</th>
      <td>581411331.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>NEW YORK</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>7</td>
      <td>2220</td>
      <td>2368</td>
      <td>2244</td>
      <td>1</td>
      <td>80</td>
      <td>2828</td>
      <td>-7.822410</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2408</th>
      <td>581411352.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>351</td>
      <td>256</td>
      <td>290</td>
      <td>0</td>
      <td>60</td>
      <td>3895</td>
      <td>-6.707317</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2411</th>
      <td>581411355.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1282</td>
      <td>1342</td>
      <td>1369</td>
      <td>0</td>
      <td>20</td>
      <td>7318</td>
      <td>-6.020942</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2412</th>
      <td>581411356.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>15</td>
      <td>5104</td>
      <td>5164</td>
      <td>5191</td>
      <td>0</td>
      <td>40</td>
      <td>7318</td>
      <td>-6.020942</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2413</th>
      <td>581411357.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1261</td>
      <td>1321</td>
      <td>1348</td>
      <td>0</td>
      <td>20</td>
      <td>7318</td>
      <td>-6.020942</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2415</th>
      <td>581411359.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>6</td>
      <td>4497</td>
      <td>4528</td>
      <td>4573</td>
      <td>0</td>
      <td>40</td>
      <td>9461</td>
      <td>2.437538</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2436</th>
      <td>581411380.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>TEXAS</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>19</td>
      <td>4715</td>
      <td>4569</td>
      <td>4658</td>
      <td>0</td>
      <td>20</td>
      <td>5327</td>
      <td>-6.064073</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2475</th>
      <td>581411415.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>16</td>
      <td>6331</td>
      <td>6483</td>
      <td>6345</td>
      <td>0</td>
      <td>10</td>
      <td>11927</td>
      <td>1.317790</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2476</th>
      <td>581411416.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>16</td>
      <td>6316</td>
      <td>6468</td>
      <td>6330</td>
      <td>0</td>
      <td>10</td>
      <td>11927</td>
      <td>1.317790</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2508</th>
      <td>581411441.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ARIZONA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>82</td>
      <td>329</td>
      <td>259</td>
      <td>1</td>
      <td>60</td>
      <td>1269</td>
      <td>-7.359307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2509</th>
      <td>581411442.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ARIZONA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>82</td>
      <td>368</td>
      <td>300</td>
      <td>0</td>
      <td>40</td>
      <td>1269</td>
      <td>-7.359307</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2514</th>
      <td>581411447.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>KANSAS CITY</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>5</td>
      <td>185</td>
      <td>139</td>
      <td>1</td>
      <td>100</td>
      <td>2619</td>
      <td>-1.869159</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2536</th>
      <td>581411461.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>20</td>
      <td>4118</td>
      <td>3970</td>
      <td>4134</td>
      <td>0</td>
      <td>10</td>
      <td>7468</td>
      <td>-2.489960</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2589</th>
      <td>581411513.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>NEW YORK</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>3071</td>
      <td>3173</td>
      <td>3058</td>
      <td>1</td>
      <td>30</td>
      <td>9235</td>
      <td>-3.241491</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2590</th>
      <td>581411514.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>115</td>
      <td>129</td>
      <td>242</td>
      <td>0</td>
      <td>20</td>
      <td>10235</td>
      <td>-2.095460</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2605</th>
      <td>581411527.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USA</td>
      <td>ATLANTA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>8</td>
      <td>2091</td>
      <td>2071</td>
      <td>2048</td>
      <td>0</td>
      <td>20</td>
      <td>2168</td>
      <td>-5.817175</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2615</th>
      <td>581411537.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>2619</td>
      <td>-1</td>
      <td>2591</td>
      <td>0</td>
      <td>40</td>
      <td>5249</td>
      <td>-7.407407</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2616</th>
      <td>581411538.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>PHILADELPHIA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>79</td>
      <td>-1</td>
      <td>99</td>
      <td>1</td>
      <td>80</td>
      <td>3247</td>
      <td>-8.436214</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2617</th>
      <td>581411539.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>105</td>
      <td>295</td>
      <td>223</td>
      <td>0</td>
      <td>20</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2618</th>
      <td>581411540.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>105</td>
      <td>247</td>
      <td>181</td>
      <td>1</td>
      <td>60</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2619</th>
      <td>581411541.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>105</td>
      <td>295</td>
      <td>223</td>
      <td>0</td>
      <td>20</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2620</th>
      <td>581411542.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>CHARLOTTE</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>105</td>
      <td>247</td>
      <td>232</td>
      <td>1</td>
      <td>100</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2622</th>
      <td>581411544.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>2639</td>
      <td>2705</td>
      <td>2591</td>
      <td>0</td>
      <td>20</td>
      <td>5249</td>
      <td>-7.407407</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2623</th>
      <td>581411545.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USACOP</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>12</td>
      <td>2639</td>
      <td>2687</td>
      <td>2591</td>
      <td>0</td>
      <td>20</td>
      <td>5249</td>
      <td>-7.407407</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2634</th>
      <td>581411556.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAEDU</td>
      <td>MARYLAND</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>3</td>
      <td>620</td>
      <td>-1</td>
      <td>534</td>
      <td>1</td>
      <td>50</td>
      <td>4949</td>
      <td>1.210654</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2639</th>
      <td>581411561.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAEDU</td>
      <td>CALIFORNIA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1283</td>
      <td>1302</td>
      <td>1330</td>
      <td>1</td>
      <td>60</td>
      <td>7318</td>
      <td>-6.020942</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2640</th>
      <td>581411562.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAEDU</td>
      <td>CALIFORNIA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>15</td>
      <td>5126</td>
      <td>5145</td>
      <td>5173</td>
      <td>1</td>
      <td>60</td>
      <td>7318</td>
      <td>-6.020942</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2662</th>
      <td>581411584.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>NASA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>215</td>
      <td>-1</td>
      <td>64</td>
      <td>1</td>
      <td>50</td>
      <td>2110</td>
      <td>-1.162791</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2663</th>
      <td>581411585.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>128</td>
      <td>-1</td>
      <td>240</td>
      <td>1</td>
      <td>30</td>
      <td>10235</td>
      <td>-2.095460</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2664</th>
      <td>581411586.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>2</td>
      <td>209</td>
      <td>-1</td>
      <td>190</td>
      <td>1</td>
      <td>100</td>
      <td>532</td>
      <td>-1.754386</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2669</th>
      <td>581411591.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>46</td>
      <td>191</td>
      <td>82</td>
      <td>1</td>
      <td>30</td>
      <td>11363</td>
      <td>-6.850054</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2670</th>
      <td>581411592.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>46</td>
      <td>191</td>
      <td>82</td>
      <td>0</td>
      <td>10</td>
      <td>11363</td>
      <td>-6.850054</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2671</th>
      <td>581411593.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>46</td>
      <td>191</td>
      <td>82</td>
      <td>0</td>
      <td>10</td>
      <td>11363</td>
      <td>-6.850054</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2683</th>
      <td>581411605.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>8</td>
      <td>1758</td>
      <td>1799</td>
      <td>1768</td>
      <td>1</td>
      <td>100</td>
      <td>6609</td>
      <td>-1.092896</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2684</th>
      <td>581411606.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>22</td>
      <td>5499</td>
      <td>5557</td>
      <td>5545</td>
      <td>0</td>
      <td>20</td>
      <td>18076</td>
      <td>-4.946012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2685</th>
      <td>581411606.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>22</td>
      <td>5499</td>
      <td>5557</td>
      <td>5545</td>
      <td>0</td>
      <td>20</td>
      <td>18076</td>
      <td>-4.946012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2686</th>
      <td>581411607.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>22</td>
      <td>5499</td>
      <td>5557</td>
      <td>5545</td>
      <td>1</td>
      <td>80</td>
      <td>18076</td>
      <td>-4.946012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2687</th>
      <td>581411607.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>OBAMA</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>22</td>
      <td>5499</td>
      <td>5557</td>
      <td>5545</td>
      <td>1</td>
      <td>80</td>
      <td>18076</td>
      <td>-4.946012</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2699</th>
      <td>581411618.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2583</td>
      <td>2672</td>
      <td>2629</td>
      <td>0</td>
      <td>20</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2700</th>
      <td>581411619.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2583</td>
      <td>2672</td>
      <td>2629</td>
      <td>1</td>
      <td>60</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2701</th>
      <td>581411620.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOV</td>
      <td>HILLARY CLINTON</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>13</td>
      <td>2583</td>
      <td>2672</td>
      <td>2629</td>
      <td>0</td>
      <td>20</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2706</th>
      <td>581411625.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAGOVHLH</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>1</td>
      <td>178</td>
      <td>-1</td>
      <td>256</td>
      <td>0</td>
      <td>20</td>
      <td>5543</td>
      <td>-2.723312</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2711</th>
      <td>581411629.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAJUD</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>10</td>
      <td>2682</td>
      <td>-1</td>
      <td>2811</td>
      <td>0</td>
      <td>20</td>
      <td>3247</td>
      <td>-8.436214</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2740</th>
      <td>581411653.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>USAPTY</td>
      <td>UNITED STATES</td>
      <td>USA</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>24</td>
      <td>5224</td>
      <td>5339</td>
      <td>5291</td>
      <td>0</td>
      <td>10</td>
      <td>6245</td>
      <td>-6.086957</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2751</th>
      <td>581411664.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
      <td>ZWE</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1510</td>
      <td>-1</td>
      <td>1495</td>
      <td>1</td>
      <td>80</td>
      <td>5442</td>
      <td>-4.434590</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2752</th>
      <td>581411665.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
      <td>ZWE</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>4</td>
      <td>1510</td>
      <td>-1</td>
      <td>1495</td>
      <td>0</td>
      <td>20</td>
      <td>5442</td>
      <td>-4.434590</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2753</th>
      <td>581411666.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>ZWE</td>
      <td>ZIMBABWE</td>
      <td>ZWE</td>
      <td></td>
      <td></td>
      <td>...</td>
      <td>9</td>
      <td>2875</td>
      <td>2927</td>
      <td>2922</td>
      <td>0</td>
      <td>40</td>
      <td>3994</td>
      <td>-3.698225</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2755</th>
      <td>581411668.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>bte</td>
      <td>BETI</td>
      <td></td>
      <td></td>
      <td>bte</td>
      <td>...</td>
      <td>8</td>
      <td>2303</td>
      <td>-1</td>
      <td>2422</td>
      <td>0</td>
      <td>20</td>
      <td>3971</td>
      <td>-1.401051</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2756</th>
      <td>581411669.0</td>
      <td>2.01609e+07</td>
      <td>201609</td>
      <td>2016</td>
      <td>2016.72</td>
      <td>bte</td>
      <td>BETI</td>
      <td></td>
      <td></td>
      <td>bte</td>
      <td>...</td>
      <td>8</td>
      <td>2303</td>
      <td>-1</td>
      <td>2433</td>
      <td>0</td>
      <td>20</td>
      <td>3971</td>
      <td>-1.401051</td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
<p>308 rows × 76 columns</p>
</div>



# Early Pipeline to Write out R Dataframe


Ways to install
```python
pip install feather-format
```

```bash
conda install feather-format -c conda-forge
```


###  **IT WORKS!!!**


```python

```


```python
import feather
path = 'my_data.feather'
feather.api.write_dataframe(testdf, path)
newtestdf = feather.api.read_dataframe(path)
```

# Leftovers; Junkyard below here


```python
results = masterListdf[masterListdf[2].str.contains(gdelt_timeString(dateInputCheck(date)))==True]
```


```python
results[2].reset_index().ix[0][2]
```


```python
results[results[2].str.contains('gkg')]
```


```python
gdelt_timeString(dateInputCheck(date))
```


```python
import re
from dateutil.parser import parse
re.search('(([\d]{4,}).*)',clean[20][-1]).group()
```


```python
if bool(4>3):
    print "Hello"
```


```python
(datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)) == parse("2016 09 18" )
```


```python
b = dateutil.parser.parse(re.search('([\d]{4,})',clean[20][-1]).group())
```


```python
matchDate = re.search('([\d]{4,})',clean[20][-1]).group()
```


```python
def time_change(current,diff):
    date = current.replace(minute=0, second=0) + timedelta(minutes=diff)
    return date.strftime("%Y%m%d%H%M%S")
    
```


```python
# pulling most current daily report

import numpy as np
import datetime
from datetime import timedelta

currentTime = datetime.datetime.now()
timeDiff = currentTime.minute / 15 

query = np.where(timeDiff == 1,time_change(currentTime,diff=15),
        np.where(timeDiff == 2, time_change(currentTime,diff=30),
                 np.where(timeDiff == 3, time_change(currentTime,diff=45),
                          time_change(currentTime,diff=0))))

baseUrl = 'http://data.gdeltproject.org/gdeltv2/' + str(query) + '.export.CSV.zip'
```


```python
data
```


```python
myzipfile.namelist()
```


```python

import zipfile


r = requests.get(baseUrl, stream=True)

# with open('gdelt.zip', 'wb') as f:
#     f.write(r.content)
# fh = open('gdelt.zip')
# g = zipfile.ZipFile(fh)
# g.extractall()

from StringIO import StringIO
zipdata = StringIO()
zipdata.write(r.content)
myzipfile = zipfile.ZipFile(zipdata,'r')
data = myzipfile.read(str(query) + '.export.CSV')
gdeltdf = pd.read_csv(StringIO(data),delimiter='\t',header=None)

```


```python
gdeltdf.columns=headers.tableId.tolist()
```


```python
gdeltdf.SOURCEURL[((gdeltdf.ActionGeo_CountryCode =='SY')|(gdeltdf.ActionGeo_CountryCode =='IZ')) & (gdeltdf.GoldsteinScale < -4)]
```


```python
text = '''
GLOBALEVENTID	INTEGER	NULLABLE	This is the ID of the event that was mentioned in the article.
EventTimeDate	INTEGER	NULLABLE	This is the 15-minute timestamp (YYYYMMDDHHMMSS) when the event being mentioned was first recorded by GDELT (the DATEADDED field of the original event record).  This field can be compared against the next one to identify events being mentioned for the first time (their first mentions) or to identify events of a particular vintage being mentioned now (such as filtering for mentions of events at least one week old).
MentionTimeDate	INTEGER	NULLABLE	This is the 15-minute timestamp (YYYYMMDDHHMMSS) of the current update.  This is identical for all entries in the update file but is included to make it easier to load the Mentions table into a database.
MentionType	INTEGER	NULLABLE	This is a numeric identifier that refers to the source collection the document came from and is used to interpret the MentionIdentifier in the next column.  In essence, it specifies how to interpret the MentionIdentifier to locate the actual document.  At present, it can hold one of the following values:o 1 = WEB (The document originates from the open web and the MentionIdentifier is a fully-qualified URL that can be used to access the document on the web).o 2 = CITATIONONLY (The document originates from a broadcast, print, or other offline source in which only a textual citation is available for the document.  In this case the MentionIdentifier contains the textual citation for the document).o 3 = CORE (The document originates from the CORE archive and the MentionIdentifier contains its DOI, suitable for accessing the original document through the CORE website).o 4 = DTIC (The document originates from the DTIC archive and the MentionIdentifier contains its DOI, suitable for accessing the original document through the DTIC website).o 5 = JSTOR (The document originates from the JSTOR archive and the MentionIdentifier contains its DOI, suitable for accessing the original document through your JSTOR subscription if your institution subscribes to it).o 6 = NONTEXTUALSOURCE (The document originates from a textual proxy (such as closed captioning) of a non-textual information source (such as a video) available via a URL and the MentionIdentifier provides the URL of the non-textual original source.  At present, this Collection Identifier is used for processing of the closed captioning streams of the Internet Archive Television News Archive in which each broadcast is available via a URL, but the URL offers access only to the video of the broadcast and does not provide any access to the textual closed captioning used to generate the metadata.  This code is used in order to draw a distinction between URL-based textual material (Collection Identifier 1 (WEB) and URL-based non-textual material like the Television News Archive).
MentionSourceName	STRING	NULLABLE	This is a human-friendly identifier of the source of the document.  For material originating from the open web with a URL this field will contain the top-level domain the page was from.  For BBC Monitoring material it will contain “BBC Monitoring” and for JSTOR material it will contain “JSTOR.”  This field is intended for human display of major sources as well as for network analysis of information flows by source, obviating the requirement to perform domain or other parsing of the MentionIdentifier field.
MentionIdentifier	STRING	NULLABLE	This is the unique external identifier for the source document.  It can be used to uniquely identify the document and access it if you have the necessary subscriptions or authorizations and/or the document is public access.  This field can contain a range of values, from URLs of open web resources to textual citations of print or broadcast material to DOI identifiers for various document repositories.  For example, if MentionType is equal to 1, this field will contain a fully-qualified URL suitable for direct access.  If MentionType is equal to 2, this field will contain a textual citation akin to what would appear in an academic journal article referencing that document (NOTE that the actual citation format will vary (usually between APA, Chicago, Harvard, or MLA) depending on a number of factors and no assumptions should be made on its precise format at this time due to the way in which this data is currently provided to GDELT – future efforts will focus on normalization of this field to a standard citation format).  If MentionType is 3, the field will contain a numeric or alpha-numeric DOI that can be typed into JSTOR’s search engine to access the document if your institution has a JSTOR subscription.
SentenceID	INTEGER	NULLABLE	The sentence within the article where the event was mentioned (starting with the first sentence as 1, the second sentence as 2, the third sentence as 3, and so on).  This can be used similarly to the CharOffset fields below, but reports the event’s location in the article in terms of sentences instead of characters, which is more amenable to certain measures of the “importance” of an event’s positioning within an article.
Actor1CharOffset	INTEGER	NULLABLE	The location within the article (in terms of English characters) where Actor1 was found.  This can be used in combination with the GKG or other analysis to identify further characteristics and attributes of the actor.  NOTE: due to processing performed on each article, this may be slightly offset from the position seen when the article is rendered in a web browser.
Actor2CharOffset	INTEGER	NULLABLE	The location within the article (in terms of English characters) where Actor2 was found.  This can be used in combination with the GKG or other analysis to identify further characteristics and attributes of the actor.  NOTE: due to processing performed on each article, this may be slightly offset from the position seen when the article is rendered in a web browser.
ActionCharOffset	INTEGER	NULLABLE	The location within the article (in terms of English characters) where the core Action description was found.  This can be used in combination with the GKG or other analysis to identify further characteristics and attributes of the actor.  NOTE: due to processing performed on each article, this may be slightly offset from the position seen when the article is rendered in a web browser.
InRawText	INTEGER	NULLABLE	This records whether the event was found in the original unaltered raw article text (a value of 1) or whether advanced natural language processing algorithms were required to synthesize and rewrite the article text to identify the event (a value of 0).  See the discussion on the Confidence field below for more details.  Mentions with a value of “1” in this field likely represent strong detail-rich references to an event.
Confidence	INTEGER	NULLABLE	Percent confidence in the extraction of this event from this article.  See the discussion in the codebook at http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf
MentionDocLen	INTEGER	NULLABLE	The length in English characters of the source document (making it possible to filter for short articles focusing on a particular event versus long summary articles that casually mention an event in passing).
MentionDocTone	FLOAT	NULLABLE	The same contents as the AvgTone field in the Events table, but computed for this particular article.  NOTE: users interested in emotional measures should use the MentionIdentifier field above to merge the Mentions table with the GKG table to access the complete set of 2,300 emotions and themes from the GCAM system.
MentionDocTranslationInfo	STRING	NULLABLE	This field is internally delimited by semicolons and is used to record provenance information for machine translated documents indicating the original source language and the citation of the translation system used to translate the document for processing.  It will be blank for documents originally in English.  At this time the field will also be blank for documents translated by a human translator and provided to GDELT in English (such as BBC Monitoring materials) – in future this field may be expanded to include information on human translation pipelines, but at present it only captures information on machine translated materials.  An example of the contents of this field might be “srclc:fra; eng:Moses 2.1.1 / MosesCore Europarl fr-en / GT-FRA 1.0”.  NOTE:  Machine translation is often not as accurate as human translation and users requiring the highest possible confidence levels may wish to exclude events whose only mentions are in translated reports, while those needing the highest-possible coverage of the non-Western world will find that these events often offer the earliest glimmers of breaking events or smaller-bore events of less interest to Western media.o SRCLC. This is the Source Language Code, representing the three-letter ISO639-2 code of the language of the original source material. o ENG.  This is a textual citation string that indicates the engine(s) and model(s) used to translate the text.  The format of this field will vary across engines and over time and no expectations should be made on the ordering or formatting of this field.  In the example above, the string “Moses 2.1.1 / MosesCore Europarl fr-en / GT-FRA 1.0” indicates that the document was translated using version 2.1.1 of the Moses   SMT platform, using the “MosesCore Europarl fr-en” translation and language models, with the final translation enhanced via GDELT Translingual’s own version 1.0 French translation and language models.  A value of “GT-ARA 1.0” indicates that GDELT Translingual’s version 1.0 Arabic translation and language models were the sole resources used for translation.  Additional language systems used in the translation pipeline such as word segmentation systems are also captured in this field such that a value of “GT-ZHO 1.0 / Stanford PKU” indicates that the Stanford Chinese Word Segmenter   was used to segment the text into individual words and sentences, which were then translated by GDELT Translingual’s own version 1.0 Chinese (Traditional or Simplified) translation and language models.
Extras	STRING	NULLABLE	This field is currently blank, but is reserved for future use to encode special additional measurements for selected material.
'''
```


```python
from StringIO import StringIO
eventMentions = pd.read_csv(StringIO(text),delimiter='\t',header=None)
```


```python
eventMentions.columns=['tableId', 'dataType','Empty', 'Description']
```


```python
eventMentions.to_csv('../../gdelt2HeaderRows/schema_csvs/GDELT_2.0_eventMentions_Column_Labels_Header_Row_Sep2016.tsv',encoding='utf-8',sep='\t')
```


```python
eventMentions
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>tableId</th>
      <th>dataType</th>
      <th>Empty</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GLOBALEVENTID</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>This is the ID of the event that was mentioned...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>EventTimeDate</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>This is the 15-minute timestamp (YYYYMMDDHHMMS...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MentionTimeDate</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>This is the 15-minute timestamp (YYYYMMDDHHMMS...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>MentionType</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>This is a numeric identifier that refers to th...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MentionSourceName</td>
      <td>STRING</td>
      <td>NULLABLE</td>
      <td>This is a human-friendly identifier of the sou...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>MentionIdentifier</td>
      <td>STRING</td>
      <td>NULLABLE</td>
      <td>This is the unique external identifier for the...</td>
    </tr>
    <tr>
      <th>6</th>
      <td>SentenceID</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>The sentence within the article where the even...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Actor1CharOffset</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>The location within the article (in terms of E...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Actor2CharOffset</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>The location within the article (in terms of E...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>ActionCharOffset</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>The location within the article (in terms of E...</td>
    </tr>
    <tr>
      <th>10</th>
      <td>InRawText</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>This records whether the event was found in th...</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Confidence</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>Percent confidence in the extraction of this e...</td>
    </tr>
    <tr>
      <th>12</th>
      <td>MentionDocLen</td>
      <td>INTEGER</td>
      <td>NULLABLE</td>
      <td>The length in English characters of the source...</td>
    </tr>
    <tr>
      <th>13</th>
      <td>MentionDocTone</td>
      <td>FLOAT</td>
      <td>NULLABLE</td>
      <td>The same contents as the AvgTone field in the ...</td>
    </tr>
    <tr>
      <th>14</th>
      <td>MentionDocTranslationInfo</td>
      <td>STRING</td>
      <td>NULLABLE</td>
      <td>This field is internally delimited by semicolo...</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Extras</td>
      <td>STRING</td>
      <td>NULLABLE</td>
      <td>This field is currently blank, but is reserved...</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Add New Fields</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
gkgdf.to_csv('../../gdelt2HeaderRows/schema_csvs/GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.tsv',encoding='utf-8',sep='\t')
```


```python
gkgdf.to_csv('GDELT_2.0_gdeltKnowledgeGraph_Column_Labels_Header_Row_Sep2016.csv',sep='\t',index=False,encoding='utf-8')
```


```python
headers.to_csv('GDELT_2.0_Events_Column_Labels_Header_Row_Sep2016.csv', index=False,encoding='utf-8')
```


```python
import pandas as pd
mentionsdf = pd.read_csv(StringIO(text),delimiter='\t',header=None)
mentionsdf.columns=headers.columns.tolist()
```


```python

```
