#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
La-Mulana HD script_decode.py modified by Alexei Baboulevitch to re-encode the .dat file.
"""

import codecs, re, unicodedata, mmap

font00 = \
        u"!\"&'(),-./0123456789:?ABCDEFGHIJKLMNOPQRSTUVWXYZ"\
        u"　]^_abcdefghijklmnopqrstuvwxyz…♪、。々「」ぁあぃいぅうぇえぉおか"\
        u"がきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほ"\
        u"ぼぽまみむめもゃやゅゆょよらりるれろわをんァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセ"\
        u"ゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリル"\
        u"レロワヲンヴ・ー一三上下不与世丘両中丸主乗乙乱乳予争事二人今介仕他付代以仮仲件会伝位低住体何作使"\
        u"供侵係保信俺倍倒値偉側偶備傷像僧元兄先光兜入全公具典内再冒冥出刀分切列初別利刻則前剣創力加助効勇"\
        u"勉動化匹十半協博印危去参双反取受叡口古召可台史右司合同名向否周呪味呼命品唯唱問喜営器噴四回囲図国"\
        u"土在地坂型域基堂報場塊塔墓増壁壇壊士声売壷変外多夜夢大天太央失奇契奥女好妊妖妻始姿娘婦子字存孤学"\
        u"宇守官宙定宝実客室宮家密寝対封専導小少尾屋屏属山岩崖崩嵐左巨己布帯帰常年幸幻幾広床底店度座庫廊廟"\
        u"弁引弟弱張強弾当形影役彼待後心必忍忘応念怒思急性怨恐息恵悔悟悪悲情惑想意愚愛感慈態憶我戦戻所扉手"\
        u"扱投抜押拝拡拳拾持指振探撃撮操支攻放敗教散数敵敷文料斧断新方旅族日早昇明昔星映時晩普晶智暗曲書最"\
        u"月有服望未末本杉村杖束来杯板析果架柱査格械棺検椿楼楽槍様槽模樹橋機欠次欲歓止正武歩歯歳歴死殊残段"\
        u"殺殿母毒毛気水氷永求汝池決治法波泥注洞洪流海消涙涯深済減湖満源溶滅滝火灯灼炎無然熱爆爪父版牛物特"\
        u"犬状狂独獄獅獣玄玉王珠現球理瓶生産用男画界略番発登白百的盤目直盾看真眼着知石研破碑示礼社祈祖神祠"\
        u"祭禁福私秘秤移種穴究空突窟立竜章竪端笛符第筒答箱範精系約納純紫細紹終経結続緑練罠罪罰義羽習翻翼老"\
        u"考者耐聖聞肉肩胸能脱腕自至船色若苦英荷華落葉蔵薇薔薬蛇血行術衛表裁装裏補製複要見覚親解言記訳証試"\
        u"話詳認誕誘語誠説読誰調論謁謎謝識議護谷貝財貧貯買貸資賢贄贖赤走起超足跡路踊蹴身車軽輝辞込辿近返迷"\
        u"追送逃通速造連進遊過道達違遠適選遺還郎部配重野量金針鉄銀銃銅録鍵鎖鏡長門閉開間関闇闘防限険陽階隠"\
        u"雄雑難雨霊青静面革靴音順領頭題顔願類風飛食館馬駄験骨高魂魔魚鳥鳴黄黒泉居転清成仏拠維視宿浮熟飾冷"\
        u"得集安割栄偽屍伸巻緒捨固届叩越激彫蘇狭浅Ⅱ［］：！？～／０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪ"\
        u"ＫＬＭＮＯＰＲＳＴＵＶＷＸＹａｂｄｅｇｈｉｌｍｏｐｒｓｔｕｘ辺薄島異温復称狙豊穣虫絶ＱＺｃｆｊｋ"\
        u"ｎｑｖｗｙｚ＋－旧了設更橫幅似確置整＞％香ü描園為渡象相聴比較掘酷艇原民雷絵南米平木秋田県湯環砂"\
        u"漠角運湿円背負構授輪圏隙草植快埋寺院妙該式判（）警告収首腰芸酒美組各演点勝観編丈夫姫救’，．霧節"\
        u"幽技師柄期瞬電購任販Á;û+→↓←↑⓪①②③④⑤⑥⑦⑧⑨<”挑朝痛魅鍛戒飲憂照磨射互降沈醜触煮疲"\
        u"素競際易堅豪屈潔削除替Ü♡*$街極"

def decode_block(b):
    b = list(b)
    d = ""
    while b:
        o = ord(b.pop(0))
        if o in [0x000A, 0x000C, 0x0020]:
            # handles LINE FEED, FORM FEED, SPACE
            if (o == 0x000C):
                s = "{FF}"
            else:
                s = unichr(o)
        elif o >= 0x0040 and o <= 0x0050:
            s = ""
            if o == 0x0040:
                cmd = "{FLAG %d:=%d}" % (ord(b[0]), ord(b[1]))
                b = b[2:]
            elif o == 0x0042:
                cmd = "{ITEM %d}" % ord(b[0])
                b = b[1:]
            elif o == 0x0044:
                cmd = "{CLS}"
            elif o == 0x0045:
                cmd = "{BR}"
            elif o == 0x0046:
                cmd = "{POSE %d}" % ord(b[0])
                b = b[1:]
            elif o == 0x0047:
                cmd = "{MANTRA %d}" % ord(b[0])
                b = b[1:]
            elif o == 0x004a:
                colors = [ord(x) for x in b[:3]]
                cmd = "{COL %03d-%03d-%03d}" % tuple(colors)
                b = b[3:] #TODO: colors not verified
            elif o == 0x004e:
                lenopts = ord(b[0])
                opts = ["%d" % ord(x) for x in b[1:lenopts+1]]
                cmd = "{CMD %s}" % "-".join(opts)
                b = b[lenopts+1:]
            elif o == 0x004f:
                cmd = "{SCENE %d}" % ord(b[0])
                b = b[1:]
            else:
                cmd = "{UNK %02x}" % o
                assert False
            s = cmd
        elif o >= 0x0100 and o <= 0x05c0:
            s = font00[o-0x0100]
        elif o == 0x05c1:
            s = "{UN"
        elif o == 0x05c2:
            s = "DEFI"
        elif o == 0x05c3:
            s = "NED}"
        else:
            s = "{UNK %04x}" % o
            assert False
        d += s
    return d

def encode_block(block):
    special_regex = r"^{([a-zA-Z]+)( (.*?))?}"

    output = []
    count = 0

    while len(block) > 0:
        match = re.match(special_regex, block)
        if match is not None:
            command = match.group(1)
            parameters = match.group(3)

            if command == "FF":
                output.append(0x000C)
            elif command == "FLAG":
                output.append(0x0040)
                output.append(0)
                output.append(0)
                # TODO:
            elif command == "ITEM":
                output.append(0x0042)
                output.append(0)
                # TODO:
            elif command == "CLS":
                output.append(0x0044);
            elif command == "BR":
                output.append(0x0045);
            elif command == "POSE":
                output.append(0x0046)
                output.append(0)
                # TODO:
            elif command == "MANTRA":
                output.append(0x0047)
                output.append(0)
                # TODO:
            elif command == "COL":
                output.append(0x004a)
                output.append(0)
                output.append(0)
                output.append(0)
                # TODO:
            elif command == "CMD":
                output.append(0x004e)
                output.append(1)
                output.append(0)
                # TODO:
            elif command == "SCENE":
                output.append(0x004f)
                output.append(0)
            elif command == "UNDEFINED":
                output.append(0x05c1)
                output.append(0x05c2)
                output.append(0x05c3)

            # not handling UNK characters since they haven't appeared in my input

            block = block[len(match.group(0)):]
        else:
            char_ord = ord(block[0])

            location_in_font = font00.find(block[0:1])
            if location_in_font != -1:
                output.append(location_in_font + 0x0100)
            else:
                output.append(char_ord)

            block = block[1:]

    return output


def decode(fin, fout):
    # first character = number of blocks
    blocks = ord(fin.read(1))
    count = 0
    
    c = fin.read(1)
    while c:
        # each block starts with the number of characters in it x 2
        o = ord(c)
        assert o % 2 == 0

        b = fin.read(o/2)

        block_header = "-" * 40 + " " + "BLOCK %d (%d) START" % (count, o/2)
        block_footer = "-" * 40 + " " + "BLOCK %d END" % (count)

        fout.write("%s\n%s\n%s\n" % (block_header, decode_block(b), block_footer))
        
        count += 1
        c = fin.read(1)
    assert count == blocks

def encode(fin, fout):
    block_regex = r"-+ BLOCK (\d+) \((\d+)\) START\n(.*?)\n-+ BLOCK (\d+) END"

    fin_string = linestring = fin.read();
    block_matches = re.findall(block_regex, fin_string, re.DOTALL)

    last_block_number = int(block_matches[-1][0]) + 1
    assert len(block_matches) == last_block_number

    encoded_blocks = [len(block_matches)]

    for block_match in block_matches:
        block_num = int(block_match[0])
        block_len = int(block_match[1])
        block_end_num = int(block_match[3])

        assert block_num == block_end_num

        print "found block number " + str(block_num) + " with length " + str(block_len)

        encoded_block = encode_block(block_match[2])
        encoded_block.insert(0, len(encoded_block) * 2)

        encoded_blocks += encoded_block

    encoded_blocks_string = ""

    for char in encoded_blocks:
        encoded_blocks_string += unichr(char)

    fout.write(encoded_blocks_string)

# with codecs.open("script_code.dat", "r", "utf_16_be") as fin:
#     with codecs.open("script_out_cmd.txt", "w", "utf_8") as fout:
#         decode(fin, fout)

# with codecs.open("script_out_cmd.txt", "r", "utf_8") as fin:
#     with codecs.open("script_code_new.dat", "w", "utf_16_be") as fout:
#         encode(fin, fout)

with codecs.open("script_code_new.dat", "r", "utf_16_be") as fin:
    with codecs.open("script_out_new_cmd.txt", "w", "utf_8") as fout:
        decode(fin, fout)
