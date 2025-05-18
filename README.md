# m4a_to_korean_txt
영어음성 m4a파일을 한국어 txt로 바꾸어 주는 무언가

### 설치과정
1. Install Whisper
<pre><code> 
pip install -U openai-whisper
</code></pre>

2. Install scoop
   
해당 [링크](https://scoop.sh/) 들어간 후 명령어 복붙.

3. Install ffmpeg
<pre><code> 
scoop install ffmpeg
</code></pre>

4.Install google Gemini api
<pre><code>
pip install -q -U google-genai
</code></pre>

### 실행과정
1. 본인의 제미나이 api키 입력
2. translate 버튼 누른 후 파일 선택창에서 원하는 영어 음성 m4a 파일 선택하면 됨
3. 해당 파이썬 파일이 위치한 곳에 final.txt 파일 형성됨. 이가 번역본 txt임.
   
#### 추신
처음 실행시 시간 오래걸림. 

