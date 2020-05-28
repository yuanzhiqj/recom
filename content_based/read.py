from __future__ import division
import os
import operator

def get_avg(input_file):
    """
    获取平均分
        args: 
            input_file:输入文件
        return:
            一个字典，key:itemid value:avg
    """
    record = {}
    score = {}
    if not os.path.exists(input_file):
        print("no path")
        return {}
    linenum = 0
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 4:
            continue
        userid, itemid, rating = item[0],item[1],float(item[2])
        if itemid not in record:
            record[itemid] = [0,0]
        record[itemid][0] += rating
        record[itemid][1] += 1
    fp.close()
    for itemid in record:
        score[itemid] = round(record[itemid][0]/record[itemid][1],3)
    return score

#item_cate[itemid]:{fix_cate:ratio}
def get_item_cate(input_file, avg_score):
    """
    得到不同种类的电影的评分排序 和 同一电影的种类
    """
    record = {}
    item_cate = {}
    cate_item_sort = {}
    linenum = 0
    topk = 100
    if not os.path.exists(input_file):
        return {},{}
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if(len(item) < 3):
            continue
        itemid = item[0]
        cate_str = item[-1]
        cate_list = cate_str.strip().split("|")
        ratio = round(1/len(cate_list),3)
        if itemid not in item_cate:
            item_cate[itemid] = {}
        for fix_cate in cate_list:
            item_cate[itemid][fix_cate] = ratio
    fp.close()

    for itemid in item_cate:
        for cate in item_cate[itemid]:
            if cate not in record:
                record[cate] = {}
            itemid_rating_score = avg_score.get(itemid,0)
            record[cate][itemid] = itemid_rating_score
    for cate in record:
        if cate not in cate_item_sort:
            cate_item_sort[cate] = []
        for combo in sorted(record[cate].items(),key=operator.itemgetter(1),reverse=True)[:topk]:
            cate_item_sort[cate].append(combo[0]+"_"+str(combo[1]))
    return item_cate, cate_item_sort

def get_latest_timestamp(input_file):
    """
    Args:
        input_file:user rating file
    only need run once
    """

    if not os.path.exists(input_file):
        return
    linenum = 0
    latest = 0
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 4:
            continue
        timestamp = int(item[3])
        if timestamp > latest:
            latest = timestamp
    fp.close()
    print(latest)

    
if __name__ == "__main__":
    avg_score = get_avg("data/ratings.txt")
    print(len(avg_score))
    print(avg_score["31"])
    item_cate, cate_item_sort = get_item_cate("data/movies.txt",avg_score)
    print(item_cate["1"])
    print(cate_item_sort["Children"])