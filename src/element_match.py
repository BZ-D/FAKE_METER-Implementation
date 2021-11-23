import cv2.cv2


# GUI Element Matching
# including Text element matching and graphical element matching


def text_match(words1, words2):
    """
    给定两个⽂本元素e1，e2
    设t1和t2分别为这两个元素的⾮占位单词的集合
    计算t1和t2之间的相似度
    """
    sim = len(set(words1) & set(words2)) / max(len(set(words1)), len(set(words2)))

    """
    相似阈值，默认取0.4
    因为两个原因：
    1)许多⽂本元素只包含⼏个单词，两个元素间即使只有⼀个单词不同也会导致sim值很小，
    把阈值设太⼤不符合实际
    2)开发者往往会将不同元素的⽂本设为不同，减少用户混淆，这会导致不同元素之间
    ⽂本相似度较小，把阈值设太小会导致匹配到⽆关联⽂本
    """
    TEXT_SIM_THRESHOLD = 0.4

    return sim >= TEXT_SIM_THRESHOLD


def graphic_match_sift(img1, img2):
    # img1 and img2 should be read by cv2.imread()
    img11 = img1.copy()
    img22 = img2.copy()

    # 创建一个SIFT对象
    # cv2.SIFT_create(, nfeatures, nOctaveLayers, contrastThreshold, edgeThreshold, sigma)
    # nfeatures：默认为0，要保留的最佳特征的数量。 特征按其分数排名（在SIFT算法中按局部对比度排序）
    # nOctaveLayers：默认为3，金字塔每组(Octave)有多少层。 3是D. Lowe纸中使用的值。
    # contrastThreshold：默认为0.04，对比度阈值，用于滤除半均匀（低对比度）区域中的弱特征。 阈值越大，检测器产生的特征越少。
    # edgeThreshold：默认为10，用来过滤边缘特征的阈值。注意，它的意思与contrastThreshold不同，edgeThreshold越大，滤出的特征越少（保留更多特征）。
    # sigma：默认为1.6，高斯金字塔中的σ。 如果使用带有软镜头的弱相机拍摄图像，则可能需要减少数量。
    sift = cv2.SIFT_create()

    # 检测特征点
    # sift.detectAndCompute(image,keypoints)
    # 返回 keypoint 和 descriptor
    # img：输入图像，单通道
    # keypoint：输出参数，保存着图像特征点，每个特征点包含如下信息：
    #       Point2f pt：坐标
    #       float size：特征点的邻域直径
    #       float angle：特征点的方向，值为[0,360度)，负值表示不使用
    #       float response;
    #       int octave：特征点所在的图像金字塔的组
    #       int class_id：用于聚类的id
    keypoints1, descriptor1 = sift.detectAndCompute(img1, None)
    keypoints2, descriptor2 = sift.detectAndCompute(img2, None)

    # 绘制特征点
    # cv2.drawKeypoint(image, keypoints, outImage, color, flags)
    # image：输入图像
    # keypoints：上面获取的特征点
    # outImage：输出图像
    # color：颜色，默认为随机颜色
    # flags：绘制点的模式
    img11 = cv2.drawKeypoints(img1, keypoints1, img11, color=(0, 0, 255))
    img22 = cv2.drawKeypoints(img2, keypoints2, img22, color=(255, 0, 0))

    cv2.namedWindow('Detected SIFT keypoints of img1', cv2.WINDOW_NORMAL)
    cv2.imshow('Detected SIFT keypoints of img1', img11)
    cv2.waitKey()

    cv2.namedWindow('Detected SIFT keypoints of img2', cv2.WINDOW_NORMAL)
    cv2.imshow('Detected SIFT keypoints of img2', img22)
    cv2.waitKey()

    # 获取 FLANN 匹配器
    FLANN_INDEX_KDTREE = 0
    indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    searchParams = dict(checks=50)
    flann = cv2.FlannBasedMatcher(indexParams, searchParams)

    # 进行匹配
    matches = flann.knnMatch(descriptor1, descriptor2, k=2)

    # 准备空的掩膜，画好的匹配项
    matchesMask = [[0, 0] for i in range(len(matches))]

    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1, 0]

    drawPrams = dict(matchColor=(0, 255, 0),
                     singlePointColor=(255, 0, 0),
                     matchesMask=matchesMask,
                     flags=0)

    # 匹配结果图片
    img3 = cv2.drawMatchesKnn(img1, keypoints1, img2, keypoints2, matches, None, **drawPrams)

    cv2.namedWindow("matches", cv2.WINDOW_NORMAL)
    cv2.imshow("matches", img3)
    cv2.waitKey()


if __name__ == '__main__':
    img1 = cv2.imread('05.png')
    img2 = cv2.imread('06.png')

    graphic_match_sift(img1, img2)
