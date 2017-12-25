#coding=utf-8

import chardet;
 
def chardet_detect_str_encoding():
    """
        Demo how to use chardet to detect string encoding/charset
    """
    inputStr = "��ǰ�ļ�ʱUTF-8��������������������ַ�����Ҳ��UTF-8�����";
    detectedEncodingDict = chardet.detect(inputStr);
    print "type(detectedEncodingDict)=",type(detectedEncodingDict); #type(detectedEncodingDict)= <type 'dict'>
    print "detectedEncodingDict=",detectedEncodingDict; #detectedEncodingDict= {'confidence': 0.99, 'encoding': 'utf-8'}
    detectedEncoding = detectedEncodingDict['encoding'];
    print "That is, we have %d%% confidence to say that the input string encoding is %s"%(int(detectedEncodingDict['confidence']*100), detectedEncoding);
 
if __name__ == '__main__':
    chardet_detect_str_encoding();
    
    