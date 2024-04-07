import time
class ConversationDirector:
    staticmethod
    def connection(ChatConnectQueue : list,searchQuery : list):
        match_user = [
            user for user in ChatConnectQueue
            if user[0] > (int(time.time()) - (20*60)) and
            user[2] in searchQuery[3] and
            searchQuery[2] in user[3]
        ]
        if len(match_user) != 0:
            result = {"status" : "finded","users" : [match_user[0][1],searchQuery[1]]}
            ChatConnectQueue.remove(match_user[0])
        else:
            ChatConnectQueue.append(searchQuery)
            result = {"status" : "create"}
        return result
        
# [time,telegram_id,c_gender,f_gender]
# [3232323,23232,M,MW]