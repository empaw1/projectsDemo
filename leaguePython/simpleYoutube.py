from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# loggin into the channel
channel = Channel()
channel.login(r'C:\Users\forry\Documents\pythonfiles\leagueRecording\client_secrets.json', r'C:\Users\forry\Documents\pythonfiles\leagueRecording\credentials.storage')

# setting up the video that is going to be uploaded
video = LocalVideo(file_path=r'C:\Users\forry\Videos\youtubetest.mkv')

# setting snippet
video.set_title("My Title")
video.set_description("This is a description")
video.set_tags(["this", "tag"])
video.set_category("gaming")
video.set_default_language("en-US")

# setting status
video.set_embeddable(True)
video.set_license("creativeCommon")
video.set_privacy_status("private")
video.set_public_stats_viewable(True)

# setting thumbnail
video.set_thumbnail_path(r"C:\Users\forry\Documents\pythonfiles\testthumbnail.jpg")
#video.set_playlist("PLDjcYN-DQyqTeSzCg-54m4stTVyQaJrGi")

# uploading video and printing the results
video = channel.upload_video(video)
print(video.id)
print(video)

# liking video
video.like()