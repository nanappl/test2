from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flask_login import login_required, current_user
from .model import db
import random

quiz = Blueprint('quiz', __name__)

QUESTIONS = [
    {"question": "Aké je hlavné mesto Francúzska?", "options": ["Paríž", "Berlín", "Madrid", "Rím"], "answer": "Paríž"},
    {"question": "Kto namaľoval Monu Lisu?", "options": ["Van Gogh", "Da Vinci", "Picasso", "Michelangelo"], "answer": "Da Vinci"},
    {"question": "Aká je najväčšia planéta v našej slnečnej sústave?", "options": ["Zem", "Mars", "Jupiter", "Saturn"], "answer": "Jupiter"},
    {"question": "Kto napísal 'Rómea a Júliu'?", "options": ["Shakespeare", "Dickens", "Hemingway", "Austen"], "answer": "Shakespeare"},
    {"question": "Aké zviera je známe ako kráľ džungle?", "options": ["Lev", "Tiger", "Slon", "Žirafa"], "answer": "Lev"},
    {"question": "Ktorý prvok má chemický symbol O?", "options": ["Kyslík", "Osmium", "Ozón", "Oxygenium"], "answer": "Kyslík"},
    {"question": "Kto vynájdol telefón?", "options": ["Einstein", "Tesla", "Bell", "Edison"], "answer": "Bell"},
    {"question": "Aký je najväčší oceán na Zemi?", "options": ["Atlantický oceán", "Tichý oceán", "Indický oceán", "Arktický oceán"], "answer": "Tichý oceán"},
    {"question": "Aká je hlavná zložka guacamole?", "options": ["Rajčina", "Avokádo", "Cibuľa", "Citrón"], "answer": "Avokádo"},
    {"question": "Ktorý slávny vedec vyvinul teóriu relativity?", "options": ["Newton", "Einstein", "Galileo", "Tesla"], "answer": "Einstein"},
    {"question": "Aká je najtvrdšia prírodná látka na Zemi?", "options": ["Zlato", "Diamant", "Železo", "Platinum"], "answer": "Diamant"},
    {"question": "V akej krajine vznikli Olympijské hry?", "options": ["Taliansko", "Francúzsko", "Grécko", "Egypt"], "answer": "Grécko"},
    {"question": "Aká je najdlhšia rieka na svete?", "options": ["Amazonka", "Níl", "Jangc'", "Mississippi"], "answer": "Amazonka"},
    {"question": "Ktoré zviera môže žiť ako vo vode, tak na zemi?", "options": ["Had", "Žaba", "Tučniak", "Velryba"], "answer": "Žaba"},
    {"question": "Aký jazyk sa najviac hovorí na svete?", "options": ["Španielčina", "Angličtina", "Mandarínština", "Francúzština"], "answer": "Mandarínština"},
    {"question": "Kto je známy ako 'Otec počítačov'?", "options": ["Turing", "Jobs", "Gates", "Babbage"], "answer": "Babbage"},
    {"question": "Aká je najmenšia krajina na svete?", "options": ["Monako", "Vatikán", "San Maríno", "Lichtenštajnsko"], "answer": "Vatikán"},
    {"question": "Ktorá planéta je známa ako 'Červená planéta'?", "options": ["Mars", "Venuša", "Jupiter", "Saturn"], "answer": "Mars"},
    {"question": "Ktoré zviera je známe svojou schopnosťou meniť farbu?", "options": ["Chameleón", "Chobotnica", "Kaliar", "Sépiová"], "answer": "Chameleón"},
    {"question": "Kto bola prvá žena, ktorá letela sólovým letom cez Atlantický oceán?", "options": ["Amelia Earhart", "Harriet Quimby", "Bessie Coleman", "Jacqueline Cochran"], "answer": "Amelia Earhart"},
    {"question": "Aké je najdlhšie pohorie na svete?", "options": ["Himaláje", "Andy", "Skalnaté hory", "Alpy"], "answer": "Andy"},
    {"question": "Ktorá krajina je najväčším producentom kávy?", "options": ["Brazília", "Vietnam", "Kolumbia", "Etiópia"], "answer": "Brazília"},
    {"question": "Aké je najvyššie zviera na Zemi?", "options": ["Slon", "Žirafa", "Kengura", "Velryba"], "answer": "Žirafa"},
    {"question": "Aká je hlavná zložka tradičného sushi?", "options": ["Ryža", "Rybka", "Riasy", "Morské plody"], "answer": "Ryža"},
    {"question": "Ktorá planéta má najviac mesiacov?", "options": ["Mars", "Zem", "Jupiter", "Saturn"], "answer": "Jupiter"},
    {"question": "Kto bol prvý človek, ktorý vstúpil na Mesiac?", "options": ["Buzz Aldrin", "Neil Armstrong", "Juri Gagarin", "Michael Collins"], "answer": "Neil Armstrong"},
    {"question": "Aká je najvyššia budova na svete?", "options": ["Empire State Building", "Burj Khalifa", "Eiffelova veža", "Petronas Towers"], "answer": "Burj Khalifa"},
    {"question": "Aký jazyk je oficiálnym jazykom Brazílie?", "options": ["Španielčina", "Portugalčina", "Angličtina", "Francúština"], "answer": "Portugalčina"},
    {"question": "Aká je najväčšia púšť na svete?", "options": ["Sahara", "Gobi", "Karakum", "Antarktická púšť"], "answer": "Antarktická púšť"},
    {"question": "Ktoré ovocie je známe ako 'kráľ ovocia'?", "options": ["Mango", "Durian", "Banán", "Ananás"], "answer": "Durian"},
    {"question": "V ktorej krajine sa nachádza Veľký bariérový útes?", "options": ["USA", "Austrália", "Nový Zéland", "Južná Afrika"], "answer": "Austrália"},
    {"question": "Ktorá slávna loď sa potopila počas svojej prvej plavby v roku 1912?", "options": ["Titanic", "Lusitania", "Britannic", "Queen Mary"], "answer": "Titanic"},
    {"question": "Aká je mena Japonska?", "options": ["Jüan", "Won", "Jen", "Ringgit"], "answer": "Jen"},
    {"question": "Aké je najľudnatejšie mesto na svete?", "options": ["New York", "Tokyo", "Londýn", "Peking"], "answer": "Tokyo"},
    {"question": "Kto objavil penicilín?", "options": ["Marie Curie", "Louis Pasteur", "Alexander Fleming", "Edward Jenner"], "answer": "Alexander Fleming"},
    {"question": "Aká je hlavná zložka hummusu?", "options": ["Cícer", "Šošovica", "Fazuľa", "Hrášok"], "answer": "Cícer"},
    {"question": "Aká je najtvrdšia časť ľudského tela?", "options": ["Kosti", "Zuby", "Nehty", "Lebka"], "answer": "Zuby"},
    {"question": "Aká je najmenšia planéta v slnečnej sústave?", "options": ["Merkúr", "Mars", "Venuša", "Pluto"], "answer": "Merkúr"},
    {"question": "Aký je jediný cicavec schopný letu?", "options": ["Netopier", "Vták", "Lietajúca veverička", "Lietajúca ryba"], "answer": "Netopier"},
    {"question": "Ktorý slávny umelec je známy svojím obrazom 'Hviezdna noc'?", "options": ["Picasso", "Van Gogh", "Monet", "Da Vinci"], "answer": "Van Gogh"},
]

@quiz.route('/quizm', methods=['GET', 'POST'])
@login_required
def quiz_page():

    if request.args.get('reset') == 'true':
        session.pop('quiz_data', None)  

    if 'quiz_data' not in session or len(session['quiz_data']['questions']) != len(QUESTIONS):
        session['quiz_data'] = {
            "questions": random.sample(QUESTIONS, len(QUESTIONS)),  
            "answered_questions": [],
            "score": 0,
            "current_index": 0,
        }

    quiz_data = session['quiz_data']

    
    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        if selected_answer:
            current_question = quiz_data['questions'][quiz_data['current_index']]

    
            if selected_answer.strip().lower() == current_question['answer'].strip().lower():
                flash('Správne!', category='success')
                quiz_data['score'] += 1
                quiz_data['answered_questions'].append(current_question) 
            else:
                flash('Nesprávne. Konec hry!', category='error')
                
                if quiz_data['score'] > current_user.max_score:
                    current_user.max_score = quiz_data['score']
                    db.session.commit()

                final_score = quiz_data['score']
                session.pop('quiz_data')  
                return render_template('quiz_result.html', user=current_user, score=final_score, max_score=current_user.max_score)

            quiz_data['current_index'] += 1
            session['quiz_data'] = quiz_data

        if quiz_data['current_index'] >= len(quiz_data['questions']):
            flash('Gratulujeme! Všetky otázky ste odpovedali správne!', category='success')
            final_score = quiz_data['score']
            if quiz_data['score'] > current_user.max_score:
                current_user.max_score = quiz_data['score']
                db.session.commit()

            session.pop('quiz_data')  
            return render_template('quiz_result.html', user=current_user, score=final_score, max_score=current_user.max_score)


    current_question = quiz_data['questions'][quiz_data['current_index']]
    return render_template('quiz.html', user=current_user, question=current_question, index=quiz_data['current_index'] + 1, total_questions=len(quiz_data['questions']))
