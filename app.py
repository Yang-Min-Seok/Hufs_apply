from flask import Flask, request, render_template, session, redirect, flash

app = Flask(__name__)

app.secret_key = 'alstjr!!98'
app.config['SESSION_TYPE'] = 'filesystem'

# 가입된 회원을 관리 해 줄 리스트
userinfo = []

@app.route('/', methods=['GET', 'POST'])
def landing():
    global userinfo

    # 로그인 세션이 있으면
    if session.get('logged_in'):
        print('로그인 기록이 존재합니다.')
        flash('로그인 기록이 존재합니다.')

        # show.html로
        return render_template('Show.html')
    
    # 로그인 세션이 없고, POST방식으로 접근했으면,
    elif request.method == 'POST':
        
        print(request.form['id'], request.form['password'])
        
        # id
        id = request.form['id']
        # password
        password = request.form['password']
        
        # 기존 회원이 맞는지 검사
        for user in userinfo:
            # 기존 회원과 일치하는 id(학번)이 있고,
            if user['user_id'] == id:
                # 비밀번호까지 같으면
                if user['user_password'] == password:
                    flash("로그인되었습니다.")
                    print('로그인되었습니다.')
                    
                    # 로그인 성공처리 후
                    session['logged_in'] = True
                    # id 세션에 기록하기
                    session['user_id'] = id

                    # name 뽑기
                    name = user['user_name']

                    # 이전에 지원한 적이 없으면,
                    if not user['user_major']:
                        
                        # apply.html로 (name 들고)
                        return render_template('Apply.html', name = name)
                    
                    # 이전에 지원한 적이 있으면,
                    # major 뽑기
                    major = user['user_major']

                    # major_cnt
                    major_cnt = 0
                    
                    # 같은 전공에 지원한 사람들을 넣어 줄 리스트
                    major_list = []

                    # 유저들 중
                    for user in userinfo:
                        # 같은 전공에 지원한 사람이 있으면,
                        if user['user_major'] == major:
                            # major_cnt 올려주고,
                            major_cnt += 1
                            # major_list에 추가
                            major_list.append(user)
                    
                    # major_list 정렬
                    major_list = sorted(major_list, key=lambda x: x['user_GPA'], reverse=True)
                    
                    # 등수 뽑기
                    rank = 1

                    # 같은 전공에 지원한 사람들 중
                    for applied in major_list:
                        # 현재 아이디랑 같으면
                        if applied['user_id'] == id:
                            # 반복문 종료
                            break
                        # 다르면
                        else:
                            # rank 올려주기
                            rank += 1

                    # Show.html로 (name, major, sum, rank 들고)
                    return render_template('Show.html', name = name, major = major, sum = major_cnt, rank=rank)
                
                # id는 맞으나 비밀번호가 틀리면
                else:
                    print('비밀번호 오류입니다.')
                    flash('비밀번호 오류입니다.')
                    # 다시 Landing.html로
                    return redirect('/')
        
        # 기존 회원에 없으면,
        print('회원 가입이 필요합니다.')
        flash('회원 가입이 필요합니다.')
        # 다시 Landing.html로
        return redirect('/')
    
    # 로그인 세션이 없고, GET 방식으로 접근했으면,
    else:
        # 현재 이용자 수
        now_user = len(userinfo)

        return render_template('Landing.html', total=now_user)

@app.route('/signin', methods=['GET', 'POST'])
def signin():

    # POST 방식으로 접근했으면 (회원 등록 버튼을 눌렀으면)
    if request.method == 'POST':
        
        # id
        id = request.form['new_id']
        
        # id 유효성 검사
        # 아무것도 안적으면
        if not len(id):
            print('학번을 적어주세요')
            flash('학번을 적어주세요')
            # 재연결
            return redirect('/signin')
        # hufs.ac.kr형식 이아니면,
        elif id[-10:-1] != 'hufs.ac.k':
            print('아이디 형식을 확인해주세요(ㅇㅇㅇ@hufs.ac.kr)')
            flash('아이디 형식을 확인해주세요(ㅇㅇㅇ@hufs.ac.kr)')

        # name
        name = request.form['new_name']
        
        # name 유효성 검사
        # 아무것도 안적으면
        if not len(name):
            print('이름을 적어주세요.')
            flash('이름을 적어주세요.')
            # 재연결
            return redirect('/signin')
        
        # password
        password = request.form['new_password']
        # check_password
        check_password = request.form['check_password']
        
        # password 유효성 검사
        # 아무것도 안적으면
        if not len(password) or not len(check_password):
            print('비밀번호 혹은 비밀번호확인을 적어주세요.')
            flash('비밀번호 혹은 비밀번호확인을 적어주세요.')
            # 재연결
            return redirect('/signin')

        # 비밀번호와 비밀번호확인이 맞지 않으면,
        elif password != check_password:
            print('비밀번호가 맞지 않습니다.')
            flash('비밀번호가 맞지 않습니다.')
            return redirect('/signin')
        
        # 비밀번호와 비밀번호 확인이 맞고,
        else:
            # 기존 유저들 정보 중
            for user in userinfo:
                # 겹치는 아이디(학번)이 있으면
                if user['user_id'] == id:
                    print('이미 가입된 회원입니다.')
                    flash('이미 가입된 회원입니다.')

                    # 현재 이용자 수
                    now_user = len(userinfo)
                    return render_template('Landing.html', total=now_user)

            # 겹치는 아이디(학번)이 없으면
            else:
                print('회원 등록이 완료 되었습니다.')
                flash('회원 등록이 완료 되었습니다.')
                print(id, name)

                # 회원 정보에 추가
                userinfo.append({
                    'user_id': id,
                    'user_name': name,
                    'user_password': password,
                    'user_major': None,
                    'user_GPA': None,
                })
                
                # 현재 이용자 수
                now_user = len(userinfo)
                
                # 다시 처음 화면으로
                return render_template('Landing.html', total=now_user)

    # GET 방식으로 접근했으면 (처음 들어왔으면)
    else:
        return render_template('Signin.html')

@app.route('/show')
def show():
    return render_template('Show.html')
    

@app.route('/logout')
def logout():
    
    # 세션 없애준 후
    session['logged_in'] = False
    # 세션 아이디 삭제
    session['user_id'] = ''
    print('성공적으로 로그아웃되었습니다.')
    flash('성공적으로 로그아웃되었습니다.')
    # 처음 화면으로 돌아가기
    return redirect('/')

@app.route('/apply', methods=['GET', 'POST'])
def apply():

    # post 방식으로 접근했으면(입력했으면,)
    if request.method == 'POST':
        
        # 전공
        major = request.form['major']
        
        # GPA
        GPA = request.form['GPA']
        
        # GPA 유효성 검사
        if GPA == '' or not 0 <= float(GPA) <= 4.5:
            print('알맞지 않은 GPA입니다.')
            flash('알맞지 않은 GPA입니다.')
            # 다시 apply화면으로
            return redirect('/apply')
        
        # 통과했으면,
        print('지원 완료',major,GPA)
        flash('모의 지원이 성공적으로 완료되었습니다. 빠른 시일 내에 인증 메일을 보내 주시기 바랍니다.')
        
        # id 뽑기
        id = session.get('user_id')
        
        # 전공, GPA 업데이트
        for user in userinfo:
            # 유저의 아이디를 찾아서
            if user['user_id'] == id:
                # 전공과 GAP 값을 넣어주기
                user['user_major'] = major
                user['user_GPA'] = float(GPA)
                # name도 뽑아주기
                name = user['user_name']
        
        # major_cnt
        major_cnt = 0
        
        # 같은 전공에 지원한 사람들을 넣어 줄 리스트
        major_list = []

        # 유저들 중
        for user in userinfo:
            # 같은 전공에 지원한 사람이 있으면,
            if user['user_major'] == major:
                # major_cnt 올려주기
                major_cnt += 1
                # major_list에 추가
                major_list.append(user)
        
        # major_list 정렬
        major_list = sorted(major_list, key=lambda x: x['user_GPA'], reverse=True)
        
        # 등수 뽑기
        rank = 1

        # 같은 전공에 지원한 사람들 중
        for applied in major_list:
            # 현재 아이디랑 같으면
            if applied['user_id'] == id:
                # 반복문 종료
                break
            # 다르면
            else:
                # rank 올려주기
                rank += 1
        

        # Show.html로(name, major, sum, rank 들고)
        return render_template('Show.html', name = name, major = major, sum = major_cnt,rank = rank)
    
    # get방식으로 접근했으면,
    else:
        # id 세션에서 얻어내기
        id = session.get('user_id')

        for user in userinfo:
            # 유저의 아이디를 찾아서
            if user['user_id'] == id:
                # name 뽑아주기
                name = user['user_name']

        # Apply 탬플릿으로(name 들고)
        return render_template('Apply.html', name = name)

# port, debug 설정
app.run(port=5001, debug=True)