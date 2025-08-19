# signalTGbot
1) brew install virtualenv только один раз
2) установить https://www.sourcetreeapp.com/ и клонировать signalTGbot только один раз
3) перейти в develop
4) кнопка ветка, создать новую ветку от девелоп 
4) открыть проект, в терминале в курсоре virtualenv venv
5) в терминале в курсоре source venv/bin/activate 
6) запуск: 
    первый запуск: 
        pip install -r requirements.txt
        python src/bot.py  (запуск в терминале, логи видны)
        nohup python -u src/bot.py > bot.log 2>&1 &  (бекграунд запуск, логи в файле bot.log)
    перезапуск после внесения изменений:
        pkill -f "src/bot.py" || true
        pip install -r requirements.txt
        nohup python -u src/bot.py > bot.log 2>&1 &
        ps aux | grep "src/bot.py" | grep -v grep 
        tail -n 100 bot.log
7) если все заебись в sourcetree коммит, затем отправить, отправляешь свою ветку в гитхаб
8) красавичк жиэс
9) перед началом работы получить девелоп из оригин в sourcetree
