from gtts import gTTS

language = 'pt-pt'

audio = gTTS(
    text = 'Só sei que nada sei',
    lang = language
)

audio.save('audio.mp3')
