# GUI Element Matching
# including Text element matching and graphical element matching

def text_match(words1, words2):
    """
    给定两个⽂本元素e1，e2
    设t1和t2分别为这两个元素的⾮占位单词的集合
    计算t1和t2之间的相似度
    """
    sim = len(set(words1) & set(words2)) \
          / \
          max(len(set(words1)), len(set(words2)))

    """
    相似阈值，默认取0.4
    因为两个原因：
    1)许多⽂本元素只包含⼏个单词，两个元素间即使只有⼀个单词不同也会导致sim值很小，
    把阈值设太⼤不符合实际
    2)开发者往往会将不同元素的⽂本设为不同，减少用户混淆，这会导致不同元素之间
    ⽂本相似度较小，把阈值设太小会导致匹配到⽆关联⽂本
    """
    TEXT_SIM_THRESHOLD = 0.4

    