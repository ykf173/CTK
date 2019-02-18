import sys
import time
from xml.dom import minidom

def sentenceAlign():
    with open(sys.argv[1], "r", encoding='utf-8') as al_file:
        no_aligns = al_file.readlines()
    al_file.close()

    with open(sys.argv[2], "r", encoding='utf-8') as en_file:
        en_lines = en_file.readlines()
    en_file.close()

    with open(sys.argv[3], "r", encoding='utf-8') as zh_file:
        zh_lines = zh_file.readlines()
    zh_file.close()

    sentencePairs = []
    for no_align in no_aligns:
        no_sentences = no_align.rstrip().lstrip(' ').replace(' ', '').split('<=>')
        no_sentence = []
        sentencePair = []

        for no in no_sentences:
            if ',' in no:
                no_sentence = no.split(',')
            else:
                no_sentence.append(no)

        if no_sentence[-1] != 'omitted' and no_sentence[0] != 'omitted':
            if len(no_sentence) == 2:
                sentencePair.append(en_lines[int(no_sentence[0])-1].strip())
                sentencePair.append(zh_lines[int(no_sentence[1])-1].strip())
                sentencePairs.append(sentencePair)

            else:
                sentencePair.append(en_lines[int(no_sentence[-2])-1].strip())
                sentencePair.append(zh_lines[int(no_sentence[-1])-1].strip())
                sentencePairs.append(sentencePair)

    generateTmx(sentencePairs)

def generateTmx(sentencePairs):
    dom = minidom.Document()
    tmx_node = dom.createElement('tmx')
    tmx_node.setAttribute('version', '1.4')
    dom.appendChild(tmx_node)

    header_node = dom.createElement('header')
    header_node.setAttribute('creationtool', 'self_create')
    header_node.setAttribute('segtype', 'sentence')
    header_node.setAttribute('o-tmf', 'TW4Win 2.0 Format')
    header_node.setAttribute('adminlang', 'EN')
    header_node.setAttribute('srclang', 'EN')
    tmx_node.appendChild(header_node)

    body_node = dom.createElement('body')
    print(len(sentencePairs))
    lotime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    for sentencePair in sentencePairs:

        tu_node = dom.createElement('tu')
        tu_node.setAttribute('creationdate', lotime)
        tu_node.setAttribute('creationid', 'self')
        tu_node.setAttribute('srclang', 'EN')

        prop_node = dom.createElement('prop')
        prop_node.setAttribute('tpye', 'Txt::Note')
        prop_value = dom.createTextNode(sys.argv[1].strip('.txt'))
        prop_node.appendChild(prop_value)

        tuv_en_node = dom.createElement('tuv')
        tuv_en_node.setAttribute('xml:lang', 'EN')
        seg_en_node = dom.createElement('seg')
        seg_en_value = dom.createTextNode(sentencePair[0])
        seg_en_node.appendChild(seg_en_value)
        tuv_en_node.appendChild(seg_en_node)

        tuv_zh_node = dom.createElement('tuv')
        tuv_zh_node.setAttribute('xml:lang', 'ZH')
        seg_zh_node = dom.createElement('seg')
        seg_zh_value = dom.createTextNode(sentencePair[1])
        seg_zh_node.appendChild(seg_zh_value)
        tuv_zh_node.appendChild(seg_zh_node)

        tu_node.appendChild(prop_node)
        tu_node.appendChild(tuv_en_node)
        tu_node.appendChild(tuv_zh_node)

        body_node.appendChild(tu_node)

    tmx_node.appendChild(body_node)

    tmx_file = sys.argv[1].strip('.txt') + '.tmx'

    try:
        with open(tmx_file, 'w', encoding='utf-8') as f_tmx:
            dom.writexml(f_tmx, indent='', addindent='\t', newl='\n', encoding='UTF-8')
        f_tmx.close()
    except Exception as err:
        print('error information：{0}'.format(err))

    # with open(tmx_file, 'r', encoding='utf-8') as f_tmx:
    #     lines = f_tmx.readlines()
    #     newLines = ''
    #     for line in lines:
    #         if line == lines[1]:
    #             newLines += '<!DOCTYPE tmx SYSTEM "tmx14a.dtd">\n'
    #
    #         newLines += line
    #
    # with open(tmx_file, 'w', encoding='utf-8') as f_tmx:
    #     f_tmx.write(newLines)

if __name__ == '__main__':
    sentenceAlign()

#问题，去除中文文本最后一个空行

#LF分句-》去空格-》chamopllion句对齐-》提取tmx