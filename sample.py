import streamlit as st
from googleapiclient.discovery import build
import pymongo
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
import mysql.connector
connect=mysql.connector.connect(
host='localhost',
user='root',
password='Guvi12345',
auth_plugin='mysql_native_password')
api_key='AIzaSyB44kjaL_TvWC4LiuTS2wr3TiV_3-JSExw'
youtube = build('youtube', 'v3', developerKey=api_key)
st.set_page_config(layout='wide')
st.title(':blue[Youtube Data Harvesting Tej]')
title = st.text_input(':red[Enter Your 11 Digit Channel_Id]')
st.write(':red[The Channel Id you enter is :]', title)
def get_channel_status(channel_id):
    all_data = []
    request = youtube.channels().list(
              part="snippet,contentDetails,statistics",
              id=channel_id)
    response = request.execute()
    for i in range(len(response['items'])):
        channel_information={
                    'channel_name':response['items'][i]['snippet']['title'],
                    'channel_id':response['items'][i]['id'],
                    'subscription_count':response['items'][i]['statistics']['subscriberCount'],
                    'channel_views':response['items'][i]['statistics']['viewCount'],
                    'Total_videos':response['items'][i]['statistics']['videoCount'],
                    'channel_description':response['items'][i]['snippet']['description'],
                    'playlist_id':response['items'][i]['contentDetails']['relatedPlaylists']['uploads']}
        all_data.append(channel_information)
    return all_data
def get_channel_videos(channel_id):
    video_ids = []
    res = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    next_page_token = None
    
    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id, 
                                           part='snippet', 
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        for i in range(len(res['items'])):
            video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = res.get('nextPageToken')
        
        if next_page_token is None:
            break
    return video_ids
def get_video_details(video_id):
    video_stats = []
    
    for i in range(0, len(video_id), 50):
        response = youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=video_id[i:i+50]).execute()
        for video in response['items']:
            video_details = dict(Channel_name = video['snippet']['channelTitle'],
                                Channel_id = video['snippet']['channelId'],
                                Video_id = video['id'],
                                Video_name = video['snippet']['title'],
                                Tags = video['snippet'].get('tags',[]),
                                Thumbnail = video['snippet']['thumbnails']['default']['url'],
                                Description = video['snippet']['description'],
                                Published_date = video['snippet']['publishedAt'],
                                Duration = video['contentDetails']['duration'],
                                Views = video['statistics']['viewCount'],
                                Likes = video['statistics'].get('likeCount',0),
                                Dislikes=video['statistics'].get('dislikeCount', 0),
                                Comments = video['statistics'].get('commentCount',0),
                                Favorite_count = video['statistics']['favoriteCount'],
                                Definition = video['contentDetails']['definition'],
                                Caption_status = video['contentDetails']['caption'])
            video_stats.append(video_details)
    return video_stats
def get_comments_in_videos(video_id):
    all_comments = []
    for video_id in video_id:
        try:
            request_comments = youtube.commentThreads().list(
            part="snippet,replies",
            maxResults=10,
            videoId=video_id)
            response_comments = request_comments.execute()
            for comment in response_comments['items']:
                comments_information= comment_information = {
                                    "Comment_Id": comment['snippet']['topLevelComment']['id'],
                                    "Comment_Text": comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                                    "Comment_Author": comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                    "Comment_PublishedAt": comment['snippet']['topLevelComment']['snippet']['publishedAt']}
                comments_in_video_info = {'video_id': video_id, 'comments': comments_information}

                all_comments.append(comments_in_video_info)
        except:
            print('Could not get comments for video ' + video_id)
    return all_comments
def entire_details():
    channel=get_channel_status(title)
    video_id=get_channel_videos(title)
    videos=get_video_details(video_id)
    comments=get_comments_in_videos(video_id)
    data={"channel_information":channel,
          "video_information":videos,
          "comments_information":comments}
    return data 
btn=st.button(':orange[data_scrab]')
if btn:
    full_details=entire_details()
    st.write(full_details)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db=client["Youtube_Data_Harvesting"]
collection=db["youtube_data_information"]
btn1=st.button(':green[store_data_mongodb]')
if btn1:
    full_details=entire_details()
    col=collection.insert_one(full_details)
    st.write(col)
def channel_sql_data():
    for i in collection.find():
        channel_data=i
        if channel_data['channel_information'][0]['channel_id']==title:
            channel_sql_details={'channel_name':channel_data['channel_information'][0]['channel_name'],
                                'channel_id':channel_data['channel_information'][0]['channel_id'],
                                'subscription_count':channel_data['channel_information'][0]['subscription_count'],
                                'channel_views':channel_data['channel_information'][0]['channel_views'],
                                'channel_description':channel_data['channel_information'][0]['channel_description'],
                                'total_video':channel_data['channel_information'][0]['Total_videos'],
                                'playlist_id':channel_data['channel_information'][0]['playlist_id']}
    channel_df=pd.DataFrame.from_dict(channel_sql_details,orient='index').T
    return channel_df
def video_sql_data():
    videos_list=[] 
    for i in collection.find():
        for j in range(1,len(i['video_information'])-1):
            video_j=i['video_information'][j]
            if video_j['Channel_id']==title:
                video_sql={'video_id':video_j['Video_id'],
                                'channel_name':video_j['Channel_name'],
                                'channel_id':video_j['Channel_id'],
                                'video_name':video_j['Video_name'],
                                'Thumbnail':video_j['Thumbnail'],
                                'publised_date':video_j['Published_date'],
                                'Description':video_j['Description'],
                                'Views':video_j['Views'],
                                'Likes':video_j['Likes'],
                                'Dislikes':video_j['Dislikes'],
                                'Comments':video_j['Comments'],
                                'Duration':video_j['Duration'],
                                'Favorite_count':video_j['Favorite_count'],
                                'Caption_status':video_j['Caption_status']}
                videos_list.append(video_sql)
    df_video=pd.DataFrame(videos_list)
    return df_video
def comment_sql_data():
    comment_list=[]
    video_id=get_channel_videos(title)
    for i in collection.find():
        for k in range(1,len(i['comments_information'])-1):
            comment_k=i['comments_information'][k]
            if comment_k['video_id'] in video_id:
                comment_sql={'video_id':comment_k['video_id'],
                                'comment_id':comment_k['comments']['Comment_Id'],
                                'comment_text':comment_k['comments']['Comment_Text'],
                                'comment_author':comment_k['comments']['Comment_Author'],
                                'comment_PublishedAt':comment_k['comments']['Comment_PublishedAt']}
                comment_list.append(comment_sql)
    comment_df=pd.DataFrame(comment_list)
    return comment_df
mycursor=connect.cursor()
mycursor.execute('create database if not exists youtube_data_harvesting')
engine=create_engine('mysql+mysqlconnector://root:Guvi12345@localhost/youtube_data_harvesting',echo=False)
btn2=st.button(':blue[Transfer the data from mongodb to sql]')
if btn2:
    ch_sql=channel_sql_data()
    ch_sql.to_sql('channel',engine,if_exists='append',index=False)
    vi_sql=video_sql_data()
    vi_sql.to_sql('video',engine,if_exists='append',index=False,dtype={'video_id ': sqlalchemy.types.VARCHAR(length=225),
                            'channel_name': sqlalchemy.types.VARCHAR(length=225),
                            'channel_id': sqlalchemy.types.VARCHAR(length=225),
                            'video_name':sqlalchemy.types.VARCHAR(length=225),
                            'Description': sqlalchemy.types.TEXT,
                            'publised_date ': sqlalchemy.types.String(length=50),
                            'Views': sqlalchemy.types.BigInteger,
                            'Likes ': sqlalchemy.types.BigInteger,
                            'Favorite_count': sqlalchemy.types.INT,
                            'Comments': sqlalchemy.types.INT,
                            'Duration': sqlalchemy.types.VARCHAR(length=1024),
                            'Thumbnail': sqlalchemy.types.VARCHAR(length=225),
                            'Caption_status': sqlalchemy.types.VARCHAR(length=225),})
    com_sql=comment_sql_data()
    com_sql.to_sql('comment',engine,if_exists='append',index=False)

question_tosql = st.selectbox(':red[**FAQ** ]',
('1. What are the names of all the videos and their corresponding channels?',
'2. Which channels have the most number of videos, and how many videos do they have?',
'3. What are the top 10 most viewed videos and their respective channels?',
'4. Which videos have the highest number of likes, and what are their corresponding channel names?',
'5. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
'6. What is the total number of views for each channel, and what are their corresponding channel names?',
'7. What are the names of all the channels that have published videos in the year 2022?',
'8. Which videos have the highest number of comments, and what are their corresponding channel names?', 
'9. How many comments were made on each video, and what are their corresponding video names?'), key = 'collection_question')
connect_for_question=mysql.connector.connect(
host='localhost',
user='root',
password='Guvi12345',
auth_plugin='mysql_native_password',
db='youtube_data_harvesting')
ques_cursor=connect_for_question.cursor()
if question_tosql == '1. What are the names of all the videos and their corresponding channels?':
    ques_cursor.execute('SELECT video.video_name,video.channel_name FROM video;')
    result_1= ques_cursor.fetchall()
    df_1=pd.DataFrame(result_1,columns=['Video_name','Channel_name']).reset_index(drop=True)
    df_1.index+1
    st.dataframe(df_1)
if question_tosql== '2. Which channels have the most number of videos, and how many videos do they have?':
    ques_cursor.execute('SELECT channel.total_video,channel.channel_name FROM channel ORDER BY channel.total_video ASC LIMIT 1;')
    result_2= ques_cursor.fetchall()
    df_2=pd.DataFrame(result_2,columns=['total_video','Channel_name']).reset_index(drop=True)
    df_2.index+1
    st.dataframe(df_2)
if question_tosql== '3. What are the top 10 most viewed videos and their respective channels?':
    ques_cursor.execute('SELECT video.channel_name,video.video_name,video.Views FROM video ORDER BY video.Views DESC LIMIT 10;')
    result_3= ques_cursor.fetchall()
    df_3=pd.DataFrame(result_3,columns=['Channel_name','Video_name','Total_views']).reset_index(drop=True)
    df_3.index+1
    st.dataframe(df_3)
    st.bar_chart(data=df_3,x='Video_name',y='Total_views')
if question_tosql== '4. Which videos have the highest number of likes, and what are their corresponding channel names?':
    ques_cursor.execute('SELECT video.Likes,video.channel_name,video.video_name FROM video ORDER BY video.Likes DESC LIMIT 1;')
    result_4= ques_cursor.fetchall()
    df_4=pd.DataFrame(result_4,columns=['Highest_like','Channel_name','Video_name']).reset_index(drop=True)
    df_4.index+1
    st.dataframe(df_4)
if question_tosql== '5. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
    ques_cursor.execute('SELECT video.video_name,video.Likes, video.Dislikes FROM video;')
    result_5= ques_cursor.fetchall()
    df_5=pd.DataFrame(result_5,columns=['Video_name','Total_likes','Total_dislike']).reset_index(drop=True)
    df_5.index+1
    st.dataframe(df_5)
if question_tosql== '6. What is the total number of views for each channel, and what are their corresponding channel names?':
    ques_cursor.execute('SELECT channel.channel_name,channel.channel_views FROM channel ORDER BY channel.channel_views DESC;')
    result_6= ques_cursor.fetchall()
    df_6=pd.DataFrame(result_6,columns=['Channel_name','Total_views']).reset_index(drop=True)
    df_6.index+1
    st.dataframe(df_6)
if question_tosql=='7. What are the names of all the channels that have published videos in the year 2022?':
     ques_cursor.execute('SELECT video.channel_name,video.video_name,video.publised_date FROM video WHERE video.publised_date =2022;')
     result_7= ques_cursor.fetchall()
     df_7=pd.DataFrame(result_7,columns=['Channel_name','Video_name','Published_date ']).reset_index(drop=True)
     df_7.index+1
     st.dataframe(df_7)
if question_tosql=='8. Which videos have the highest number of comments, and what are their corresponding channel names?':
     ques_cursor.execute('SELECT video.channel_name,video.video_name,video.Comments FROM video ORDER BY video.Comments DESC LIMIT 1;')
     result_8= ques_cursor.fetchall()
     df_8=pd.DataFrame(result_8,columns=['Channel_name','Video_name','Highest_comment']).reset_index(drop=True)
     df_8.index+1
     st.dataframe(df_8)
if question_tosql=='9. How many comments were made on each video, and what are their corresponding video names?':
    ques_cursor.execute('SELECT video.channel_name,video.video_name,video.Comments FROM video;')
    result_9= ques_cursor.fetchall()
    df_9=pd.DataFrame(result_9,columns=['Channel_name','Video_name','Total_comment']).reset_index(drop=True)
    df_9.index+1
    st.dataframe(df_9)
    st.bar_chart(data=df_9,x='Video_name',y='Total_comment')