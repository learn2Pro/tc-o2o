# -*- coding: utf-8 -*-
# filename: get_feature.py

##################抽取如下特征,浏览数、收藏数、购物车、购买数、平均活跃天数、最后活跃天数距离最终时间的天数,先不考虑平均活跃天数####

import csv

reader_off = csv.reader(file("./o2o_data/ccf_offline_stage1_train.csv", 'rb'))
reader_on = csv.reader(file("./o2o_data/ccf_online_stage1_train.csv", 'rb'))
writer = csv.writer(file("./o2o_data/train_features.csv", 'wb'))
###################################定义统计变量###########################################
###online#######
user_coupon_pair = set()  # (u,i)对

user_get = dict()
user_click = dict()
user_buy = dict()
user_day_dis = dict()  # 用户领取day 消费day时间间隔

coupon_get = dict()  # 优惠劵领取次数
coupon_click = dict()
coupon_buy = dict()  # 优惠劵购买次数
coupon_day_dis = dict()  # 优惠劵购买日期差
coupon_discount_rate = dict()

merchant_get = dict()  # 优惠劵领取次数
merchant_click = dict()
merchant_buy = dict()  # 优惠劵购买次数
merchant_day_dis = dict()  # 优惠劵购买日期差

user_coupon_get = dict()  # (u,i)领取次数
user_coupon_click = dict()  # (u,i)点击次数
user_coupon_buy = dict()  # (u,i)购买次数
user_coupon_day_dis = dict()  # (u,i)领取次数
user_coupon_discount_rate = dict()  # (u,i)领取次数

user_merchant_get = dict()  # (u,i)领取次数
user_merchant_click = dict()  # (u,i)点击次数
user_merchant_buy = dict()  # (u,i)购买次数
user_merchant_day_dis = dict()  # (u,i)领取次数

####offline######
user_off_buy = dict()
user_off_day_dis = dict()
user_off_distance = dict()

user_coupon_off_buy = dict()
user_coupon_off_day_dis = dict()
user_coupon_off_distance = dict()
user_coupon_off_discount_rate = dict()

user_merchant_off_buy = dict()
user_merchant_off_day_dis = dict()
user_merchant_off_distance = dict()

coupon_off_buy = dict()
coupon_off_day_dis = dict()
coupon_off_distance = dict()
coupon_off_discount_rate = dict()

merchant_off_buy = dict()
merchant_off_day_dis = dict()
merchant_off_distance = dict()
num = 0
###################################初始化#############################
############################################offline#############################
num = 0
for line in reader_off:
    num += 1
    if num == 1:
        continue
    if line[2] is not None and line[2] != "null" and line[4] is not None and \
                    line[3] is not None and line[3] != "null" and line[6] is not None and line[6] != "null":
        if line[3] is not None:
            if ":" not in line[3]:
                rate = line[3]
            else:
                discount = line[3].split(":")
                rate = float("%.2f" % (float(discount[1]) / float(discount[0])))
        user_coupon_pair.add((line[0], line[1], line[2], rate, line[4]))

    if line[6] is not None and line[6] != "null":
        if line[0] not in user_off_buy:
            user_off_buy[line[0]] = 1
        else:
            user_off_buy[line[0]] += 1
        if line[1] not in merchant_off_buy:
            merchant_off_buy[line[1]] = 1
        else:
            merchant_off_buy[line[1]] += 1
        if line[1] is not None and line[1] != "null":
            if (line[0], line[1]) not in user_merchant_off_buy:
                user_merchant_off_buy[(line[0], line[1])] = 1
            else:
                user_merchant_off_buy[(line[0], line[1])] += 1
        if line[2] is not None and line[2] != "null":
            if line[2] not in coupon_off_buy:
                coupon_off_buy[line[2]] = 1
            else:
                coupon_off_buy[line[2]] += 1
            if (line[0], line[2]) not in user_coupon_off_buy:
                user_coupon_off_buy[(line[0], line[2])] = 1
            else:
                user_coupon_off_buy[(line[0], line[2])] += 1
    if line[3] is not None and line[3] != "null" and line[2] is not None and line[2] != "null":
        if ":" not in line[3]:
            rate = line[3]
        else:
            discount = line[3].split(":")
            rate = float("%.2f" % (float(discount[1]) / float(discount[0])))
        if (line[2], rate) not in coupon_off_discount_rate:
            coupon_off_discount_rate[line[2], rate] = 1
        else:
            coupon_off_discount_rate[line[2], rate] += 1
        if line[6] is not None and line[6] != "null":
            if (line[0], line[2], rate) not in user_coupon_off_discount_rate:
                user_coupon_off_discount_rate[(line[0], line[2], rate)] = 1
            else:
                user_coupon_off_discount_rate[(line[0], line[2], rate)] += 1
    if line[4] is not None and line[4] != "null" and line[6] is not None and line[6] != "null":
        if (line[0], line[4]) not in user_off_distance:
            user_off_distance[(line[0], line[4])] = 1
        else:
            user_off_distance[(line[0], line[4])] += 1
        if (line[1], line[4]) not in merchant_off_distance:
            merchant_off_distance[(line[1], line[4])] = 1
        else:
            merchant_off_distance[(line[1], line[4])] += 1
        if line[2] is not None and line[2] != "null":
            if (line[2], line[4]) not in coupon_off_distance:
                coupon_off_distance[(line[2], line[4])] = 1
            else:
                coupon_off_distance[(line[2], line[4])] += 1
        if (line[0], line[1], line[4]) not in user_merchant_off_distance:
            user_merchant_off_distance[(line[0], line[1], line[4])] = 1
        else:
            user_merchant_off_distance[(line[0], line[1], line[4])] += 1
        if line[6] is not None and line[6] != "null":
            if (line[0], line[2], line[4]) not in user_coupon_off_distance:
                user_coupon_off_distance[(line[0], line[2], line[4])] = 1
            else:
                user_coupon_off_distance[(line[0], line[2], line[4])] += 1
    if (line[5] is not None and line[5] != r"null") and (line[6] is not None and line[6] != r"null"):
        day_dis = int(line[6][4:6] - line[5][4:6]) * 30 + int(line[6][7:-1] - line[5][7:-1])
        if (line[0], day_dis) not in user_off_day_dis:
            user_off_day_dis[(line[0], day_dis)] = 1
        else:
            user_off_day_dis[(line[0], day_dis)] += 1
        if (line[1], day_dis) not in merchant_off_day_dis:
            merchant_off_day_dis[(line[1], day_dis)] = 1
        else:
            merchant_off_day_dis[(line[1], day_dis)] += 1
        if (line[2], day_dis) not in coupon_off_day_dis:
            coupon_off_day_dis[(line[2], day_dis)] = 1
        else:
            coupon_off_day_dis[(line[2], day_dis)] += 1
        if (line[0], line[2], day_dis) not in user_coupon_off_day_dis:
            user_coupon_off_day_dis[(line[0], line[2], day_dis)] = 1
        else:
            user_coupon_off_day_dis[(line[0], line[2], day_dis)] += 1
        if (line[0], line[1], day_dis) not in user_merchant_off_day_dis:
            user_merchant_off_day_dis[(line[0], line[1], day_dis)] = 1
        else:
            user_merchant_off_day_dis[(line[0], line[1], day_dis)] += 1
###################################online#############################
for line in reader_on:
    num += 1
    if num == 1:
        continue
    if line[3] is not None and line[3] != "null" and line[4] is not None and line[4] == r"null":
        if ":" not in line[4]:
            rate = line[4]
        else:
            discount = line[4].split(":")
            rate = float("%.2f" % (float(discount[1]) / float(discount[0])))
        user_coupon_pair.add((line[0], line[1], line[3], rate, "null"))

    ###########设置交互，click,get,buy (user,coupon,merchant)########
    if line[6] is not None and line[6] != "null":
        if (line[0], line[1]) is not None and line[1] != "null":
            if (line[0], line[1]) not in user_merchant_buy:
                user_merchant_buy[(line[0], line[1])] = 1
            else:
                user_merchant_buy[(line[0], line[1])] += 1
        if line[0] not in user_buy:
            user_buy[line[0]] = 1
        else:
            user_buy[line[0]] += 1
        if line[1] not in merchant_buy:
            merchant_buy[line[1]] = 1
        else:
            merchant_buy[line[1]] += 1
    if line[2] == 0:
        if line[3] is not None and line[3] != "null":
            if (line[0], line[3]) not in user_coupon_click:
                user_coupon_click[(line[0], line[3])] = 1
            else:
                user_coupon_click[(line[0], line[3])] += 1
        if line[1] is not None and line[1] != "null":
            if (line[0], line[1]) not in user_merchant_click:
                user_merchant_click[(line[0], line[1])] = 1
            else:
                user_merchant_click[(line[0], line[1])] += 1
        if line[0] not in user_click:
            user_click[line[0]] = 1
        else:
            user_click[line[0]] += 1
        if line[3] not in coupon_click:
            coupon_click[line[3]] = 1
        else:
            coupon_click[line[3]] += 1
        if line[1] not in merchant_click:
            merchant_click[line[1]] = 1
        else:
            merchant_click[line[1]] += 1
    elif line[2] == 1:
        if line[3] is not None and line[3] != "null":
            if (line[0], line[3]) not in user_coupon_buy:
                user_coupon_buy[(line[0], line[3])] = 1
            else:
                user_coupon_buy[(line[0], line[3])] += 1
            if line[3] not in coupon_buy:
                coupon_buy[line[3]] = 1
            else:
                coupon_buy[line[3]] += 1
    elif line[2] == 2:
        if line[3] is not None and line[3] != "null":
            if (line[0], line[3]) not in user_coupon_get:
                user_coupon_get[(line[0], line[3])] = 1
            else:
                user_coupon_get[(line[0], line[3])] += 1
        if (line[0], line[1]) is not None and line[1] != "null":
            if (line[0], line[1]) not in user_merchant_get:
                user_merchant_get[(line[0], line[1])] = 1
            else:
                user_merchant_get[(line[0], line[1])] += 1
        if line[0] not in user_get:
            user_get[line[0]] = 1
        else:
            user_get[line[0]] += 1
        if line[3] not in coupon_get:
            coupon_get[line[3]] = 1
        else:
            coupon_get[line[3]] += 1
        if line[1] not in merchant_get:
            merchant_get[line[1]] = 1
        else:
            merchant_get[line[1]] += 1
            ###########设置优惠力度(user,coupon,merchant)########
    if line[4] is not None and line[4] != r"null":
        if ":" not in line[4]:
            rate = line[4]
        else:
            discount = line[4].split(":")
            rate = float("%.2f" % (float(discount[1]) / float(discount[0])))
        if (line[3], rate) not in coupon_discount_rate:
            coupon_discount_rate[(line[3], rate)] = 1
        else:
            coupon_discount_rate[(line[3], rate)] += 1
        if line[6] is not None and line[6] != r"null":
            if (line[0], line[3], rate) not in user_coupon_discount_rate:
                user_coupon_discount_rate[(line[0], line[3], rate)] = 1
            else:
                user_coupon_discount_rate[(line[0], line[3], rate)] += 1
    if (line[5] is not None and line[5] != r"null") and (line[6] is not None and line[6] != r"null"):
        day_dis = int(line[6][4:6] - line[5][4:6]) * 30 + int(line[6][7:-1] - line[5][7:-1])
        if (line[0], day_dis) not in user_day_dis:
            user_day_dis[(line[0], day_dis)] = 1
        else:
            user_day_dis[(line[0], day_dis)] += 1
        if (line[3], day_dis) not in coupon_day_dis:
            coupon_day_dis[(line[3], day_dis)] = 1
        else:
            coupon_day_dis[(line[3], day_dis)] += 1
        if (line[1], day_dis) not in merchant_day_dis:
            merchant_day_dis[(line[1], day_dis)] = 1
        else:
            merchant_day_dis[(line[1], day_dis)] += 1
        if (line[0], line[3], day_dis) not in user_coupon_day_dis:
            user_coupon_day_dis[(line[0], line[3], day_dis)] = 1
        else:
            user_coupon_day_dis[(line[0], line[3], day_dis)] += 1
        if (line[0], line[2], day_dis) not in user_merchant_day_dis:
            user_merchant_day_dis[(line[0], line[2], day_dis)] = 1
        else:
            user_merchant_day_dis[(line[0], line[2], day_dis)] += 1

#############################################统计特征##########################
for k in user_coupon_pair:
    #########交互的优惠券和使用之比##############
    f_user_buy_action_ratio = 0.0
    f_coupon_buy_action_ratio = 0.0
    f_merchant_buy_action_ratio = 0.0
    f_user_action = 0
    f_user_buy = 0
    if user_click.get(k[0]) is not None:
        f_user_action += user_click.get(k[0])
    if user_get.get(k[0]) is not None:
        f_user_action += user_get.get(k[0])
    if user_buy.get(k[0]) is not None:
        f_user_action += user_buy.get(k[0])
        f_user_buy += user_buy.get(k[0])
    if user_off_buy.get(k[0]) is not None:
        f_user_action += user_off_buy.get(k[0])
        f_user_buy += user_off_buy.get(k[0])
    if f_user_action != 0:
        #####商家 交互购买比#######
        f_user_buy_action_ratio = float("%.2f" % (f_user_buy / f_user_action))
    f_coupon_action = 0
    f_coupon_buy = 0
    if coupon_click.get(k[2]) is not None:
        f_coupon_action += coupon_click.get(k[2])
    if coupon_get.get(k[2]) is not None:
        f_coupon_action += coupon_get.get(k[2])
    if coupon_buy.get(k[2]) is not None:
        f_coupon_action += coupon_buy.get(k[2])
        f_coupon_buy += coupon_buy.get(k[2])
    if coupon_off_buy.get(k[2]) is not None:
        f_coupon_action += coupon_off_buy.get(k[2])
        f_coupon_buy += coupon_off_buy.get(k[2])
    if f_user_action != 0:
        #####优惠劵 交互购买比#######
        f_coupon_buy_action_ratio = float("%.2f" % (f_coupon_buy / f_user_action))
    f_merchant_action = 0
    f_merchant_buy = 0
    if merchant_click.get(k[1]) is not None:
        f_merchant_action += merchant_click.get(k[1])
    if merchant_get.get(k[1]) is not None:
        f_merchant_action += merchant_get.get(k[1])
    if merchant_buy.get(k[1]) is not None:
        f_merchant_action += merchant_buy.get(k[1])
        f_merchant_buy += merchant_buy.get(k[1])
    if merchant_off_buy.get(k[1]) is not None:
        f_merchant_action += merchant_off_buy.get(k[1])
        f_merchant_buy += merchant_off_buy.get(k[1])
    if f_merchant_action != 0:
        #####商家 交互购买比#######
        f_merchant_buy_action_ratio = float("%.2f" % (f_merchant_buy / f_merchant_action))
    ######点击购买比，领取购买比#############
    f_user_buy_click_ratio = 0.0
    f_user_buy_get_ratio = 0.0
    f_coupon_buy_click_ratio = 0.0
    f_coupon_buy_get_ratio = 0.0
    f_merchant_buy_click_ratio = 0.0
    f_merchant_buy_get_ratio = 0.0
    if user_click.get(k[0]) is not None and user_buy.get(k[0]) is not None:
        f_user_buy_click_ratio = float("%.2f" % (user_buy.get(k[0]) / user_click.get(k[0])))
    if user_get.get(k[0]) is not None and user_buy.get(k[0]) is not None:
        f_user_buy_get_ratio = float("%.2f" % (user_buy.get(k[0]) / user_get.get(k[0])))
    if coupon_click.get(k[2]) is not None and coupon_buy.get(k[2]) is not None:
        f_coupon_buy_click_ratio = float("%.2f" % (coupon_buy.get(k[2]) / coupon_click.get(k[2])))
    if coupon_get.get(k[2]) is not None and coupon_buy.get(k[2]) is not None:
        f_coupon_buy_get_ratio = float("%.2f" % (coupon_buy.get(k[2]) / coupon_get.get(k[2])))
    if merchant_click.get(k[1]) is not None and merchant_buy.get(k[1]) is not None:
        f_merchant_buy_click_ratio = float("%.2f" % (merchant_buy.get(k[1]) / merchant_click.get(k[1])))
    if merchant_get.get(k[1]) is not None and merchant_buy.get(k[1]) is not None:
        f_merchant_buy_get_ratio = float("%.2f" % (merchant_buy.get(k[1]) / merchant_get.get(k[1])))
    ######使用优惠劵购买占比###########
    f_buy_coupon_ratio = 0.0
    f_buy_merchant_ratio = 0.0
    f_off_buy_coupon_ratio = 0.0
    f_off_buy_merchant_ratio = 0.0
    f_user_coupon_discount_ratio = 0.0
    f_user_coupon_off_discount_ratio = 0.0
    f_user_coupon_distance_ratio = 0.0
    if user_buy.get(k[0]) is not None and user_coupon_buy[(k[0], k[2])] is not None:
        f_buy_coupon_ratio = float("%.2f" % (user_buy.get(k[0]) / user_coupon_buy.get((k[0], k[2]))))
    if user_buy.get(k[0]) is not None and user_merchant_buy[(k[0], k[1])] is not None:
        f_buy_merchant_ratio = float("%.2f" % (user_buy.get(k[0]) / user_merchant_buy.get((k[0], k[1]))))
    if user_off_buy.get(k[0]) is not None and user_coupon_off_buy[(k[0], k[2])] is not None:
        f_off_buy_coupon_ratio = float("%.2f" % (user_off_buy.get(k[0]) / user_coupon_off_buy.get((k[0], k[2]))))
    if user_off_buy.get(k[0]) is not None and user_merchant_off_buy[(k[0], k[1])] is not None:
        f_off_buy_merchant_ratio = float("%.2f" % (user_off_buy.get(k[0]) / user_merchant_off_buy.get((k[0], k[1]))))
    if user_coupon_discount_rate.get((k[0], k[2], k[3])) is not None and user_buy.get(k[0]) is not None:
        f_user_coupon_discount_ratio = float(
            "%.2f" % (user_coupon_discount_rate.get((k[0], k[2], k[3])) / user_buy.get(k[0])))
    if user_coupon_off_discount_rate.get((k[0], k[2], k[3])) is not None and user_off_buy.get(k[0]) is not None:
        f_user_coupon_off_discount_ratio = float(
            "%.2f" % (user_coupon_off_discount_rate.get((k[0], k[2], k[3])) / user_off_buy[k[0]]))
    if user_coupon_off_distance.get((k[0], k[2], k[4])) is not None and user_off_distance.get((k[0], k[4])) is not None:
        f_user_coupon_distance_ratio = float(
            "%.2f" % (user_coupon_off_distance.get((k[0], k[2], k[4])) / user_off_distance.get((k[0], k[4]))))

    writer.writerow(
        (k[0], k[2], user_click[k[0]], user_get[k[0]], user_buy[k[0]], merchant_get[k[1]], merchant_click[k[1]],
         merchant_buy[k[1]], coupon_click[k[2]], coupon_get[k[1]], coupon_buy[k[2]],
         user_coupon_click[(k[0], k[2])],
         user_coupon_get[(k[0], k[2])], user_coupon_buy[(k[0], k[2])], user_off_buy[k[0]], user_off_distance[k[0]],
         coupon_off_buy[k[1]], coupon_off_distance[k[1]], user_coupon_off_buy[(k[0], k[2])],
         user_coupon_off_distance[(k[0], k[2])],
         f_user_buy_action_ratio, f_coupon_buy_action_ratio, f_merchant_buy_action_ratio, f_user_buy_click_ratio,
         f_user_buy_get_ratio, f_coupon_buy_click_ratio, f_coupon_buy_get_ratio, f_coupon_buy_click_ratio,
         f_merchant_buy_click_ratio, f_merchant_buy_get_ratio, f_buy_coupon_ratio, f_buy_merchant_ratio,
         f_off_buy_coupon_ratio,
         f_off_buy_merchant_ratio, f_user_coupon_discount_ratio, f_user_coupon_off_discount_ratio,
         f_user_coupon_distance_ratio,
         user_day_dis[k[0]], user_coupon_day_dis[(k[0], k[2])], user_off_day_dis[k[0]],
         user_coupon_off_day_dis[(k[0], k[2])]))
    ####################39维特征##################################
