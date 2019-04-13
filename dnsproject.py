import os
import operator
import csv
import re
import math

# For a given page,

# a. Count the number of unique DNS requests
# b. Print out the unique DNS names observed
# c. Print out the time the first requested webpage was visited
# d. List the URLs

# ( google.com. [15:01:56.574])
# ( yahoo.com.  [15:03:59.616])
# ( baidu.cn.   [15:06:06.930])
# ( bing.com.   [15:07:46.329])
# ( yandex.ru.  [15:09:28.903])

unique_DNS= []
first_request_time = []
last_domain = []
URLs= []
time = 0
current_time = 0
string = ''
minutes = 0.0
current_minutes = 0.0


with open('dnslog.txt' , 'r+') as f:
    for line in f:
        line = line.split()
        time = line[1].split(":")
        minutes = float(time[1])                                                 # set minutes to check for negative jumpes
        time = float(time[2])                                                    # set seconds to check for jumpes
        domain = line[7]
        if (domain != last_domain):                                              # make a big list of all nonsequential domains
            URLs.append(domain)
            last_domain = domain
        else:
            last_domain = domain
        if (time - current_time) > 5 or ((minutes - current_minutes) > 0 and (time - current_time) > -58):  # check conditions for unique_dns request
            if (len(domain.split('.')) <= 3 and domain != '') or (domain.split('.')[0]== 'www' and domain != ''):                                           # check more conditions for unique_dns request (to be certain)
                if (domain.split('.')[0] == 'www' and domain.split('.')[1] not in str(unique_DNS)) or (domain.split('.')[2] == '' and domain.split('.')[0] not in str(unique_DNS)):
                    request_time = line[0] + ' ' + line[1]
                    unique_DNS.append(domain)
                    first_request_time.append(request_time)
        current_time = time
        current_minutes = minutes


fo = open('report.txt' , 'w')
a = 0
b = 0
numbered_list = 2
count = 0
count2 = 0
last_index = 0                                                                   # save index of last unique_DNS request
for url in URLs:
    if url == unique_DNS[a]:
        if a == len(unique_DNS) - 1:                                             # for last unique_DNS only
            count2 = len(URLs) - URLs.index(unique_DNS[a])                       # count sub urls inbetween unique_DNS requests for last unique_DNS request
            last_index = URLs.index(unique_DNS[a])
            fo.write(str(unique_DNS[a]) + ': ' + str(count2) + ' Time: ' + str(first_request_time[b]) + '\n')
            break
        count = URLs.index(unique_DNS[a+1]) - URLs.index(unique_DNS[a])          # count sub urls inbetween unique_DNS requests
        fo.write(str(unique_DNS[a]) + ': ' + str(count) + ' Time: ' + str(first_request_time[b]) + '\n')
        numbered_list = 2
        fo.write('1 . ' + str(unique_DNS[a]) + '\n')
        if a != len(unique_DNS) -1:
            a += 1
            b += 1
    else:
        fo.write(str(numbered_list) + '. ' + str(url) + '\n')
        numbered_list += 1

numbered_list = 1
for url in URLs:                                                                 # collect sub_domains of last unique_DNS request
    if URLs.index(url) >= last_index:                                            # only index after last unique_DNS request in URLs
        fo.write(str(numbered_list) + '. ' + str(url) + '\n')
        numbered_list += 1

fo.close()

unique_DNS= []
first_request_time = []
last_domain = []
URLs= []
time = 0
current_time = 0
string = ''
minutes = 0.0
current_minutes = 0.0

with open('dnslog_with_blocking.txt' , 'r+') as f:
    for line in f:
        line = line.split()
        time = line[1].split(":")
        minutes = float(time[1])                                                 # set minutes to check for negative jumpes
        time = float(time[2])                                                    # set seconds to check for jumpes
        domain = line[7]
        if (domain != last_domain):                                              # make a big list of all nonsequential domains
            URLs.append(domain)
            last_domain = domain
        else:
            last_domain = domain
        if (time - current_time) > 5 or ((minutes - current_minutes) > 0 and (time - current_time) > -58):  # check conditions for unique_dns request
            if (len(domain.split('.')) <= 3 and domain != '') or (domain.split('.')[0]== 'www' and domain != ''):                                           # check more conditions for unique_dns request (to be certain)
                if (domain.split('.')[0] == 'www' and domain.split('.')[1] not in str(unique_DNS)) or (domain.split('.')[2] == '' and domain.split('.')[0] not in str(unique_DNS)):
                    request_time = line[0] + ' ' + line[1]
                    unique_DNS.append(domain)
                    first_request_time.append(request_time)
        current_time = time
        current_minutes = minutes

fob = open('report_with_blocking.txt', 'w')
a = 0
b = 0
numbered_list = 2
count = 0
count2 = 0
last_index = 0  # save index of last unique_DNS request
for url in URLs:
    if url == unique_DNS[a]:
        if a == len(unique_DNS) - 1:  # for last unique_DNS only
            count2 = len(URLs) - URLs.index(
                unique_DNS[a])  # count sub urls inbetween unique_DNS requests for last unique_DNS request
            last_index = URLs.index(unique_DNS[a])
            fob.write(str(unique_DNS[a]) + ': ' + str(count2) + ' Time: ' + str(first_request_time[b]) + '\n')
            break
        count = URLs.index(unique_DNS[a + 1]) - URLs.index(
            unique_DNS[a])  # count sub urls inbetween unique_DNS requests
        fob.write(str(unique_DNS[a]) + ': ' + str(count) + ' Time: ' + str(first_request_time[b]) + '\n')
        numbered_list = 2
        fob.write('1 . ' + str(unique_DNS[a]) + '\n')
        if a != len(unique_DNS) - 1:
            a += 1
            b += 1
    else:
        fob.write(str(numbered_list) + '. ' + str(url) + '\n')
        numbered_list += 1

numbered_list = 1
for url in URLs:  # collect sub_domains of last unique_DNS request
    if URLs.index(url) >= last_index:  # only index after last unique_DNS request in URLs
        fob.write(str(numbered_list) + '. ' + str(url) + '\n')
        numbered_list += 1

fob.close()