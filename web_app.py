"""
Web Application for AI Chatbot - Flask-based web interface.
Powered by Google Gemini Flash 2.5
"""

from flask import Flask, render_template, request, jsonify, session
import os
import secrets

from chatbot import SmartChatbot
from analytics import ConversationAnalytics, ReportGenerator
from ai_client import GeminiAIClient

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Global storage for chatbot instances (in production, use Redis/database)
chatbot_instances = {}


def get_chatbot(session_id):
    """Get or create a chatbot instance for the session."""
    if session_id not in chatbot_instances:
        chatbot_instances[session_id] = SmartChatbot()
    return chatbot_instances[session_id]


@app.route('/')
def index():
    """Render the main chat interface."""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(8)
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        session_id = session.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        
        # Get response from chatbot
        result = chatbot.chat(message)
        
        return jsonify({
            'response': result['response'],
            'sentiment': result['sentiment'],
            'mood_shift': result.get('mood_shift_detected'),
            'ui_hints': result.get('ui_hints', {}),
            'state': result.get('state', {})
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get conversation statistics."""
    try:
        session_id = session.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        stats = chatbot.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/summary', methods=['GET'])
def get_summary():
    """Get AI-generated conversation summary."""
    try:
        session_id = session.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        summary = chatbot.get_conversation_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/keywords', methods=['GET'])
def get_keywords():
    """Get AI-extracted keywords."""
    try:
        session_id = session.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        keywords = chatbot.get_keywords()
        return jsonify(keywords)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/trends', methods=['GET'])
def get_trends():
    """Get sentiment trend analysis."""
    try:
        session_id = session.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        analytics = ConversationAnalytics(chatbot.ai_client)
        sentiment_history = chatbot.get_sentiment_history()
        trends = analytics.analyze_trends(sentiment_history)
        return jsonify(trends.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/graph', methods=['GET'])
def get_graph():
    """Get ASCII mood graph."""
    try:
        session_id = session.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        sentiment_history = chatbot.get_sentiment_history()
        
        if not sentiment_history:
            return jsonify({
                'graph': '📊 No conversation data yet.\n\nStart chatting to see your mood graph!\n\nThe graph will show:\n• Your emotional journey over time\n• Sentiment trends (positive/neutral/negative)\n• Visual representation of mood shifts'
            })
        
        analytics = ConversationAnalytics(chatbot.ai_client)
        graph = analytics.generate_mood_graph(sentiment_history)
        return jsonify({'graph': graph})
    except Exception as e:
        return jsonify({'graph': f'Error generating graph: {str(e)}\n\nPlease try again after sending a few messages.'}), 200


@app.route('/profile', methods=['GET'])
def get_profile():
    """Get emotion profile."""
    try:
        session_id = session.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        analytics = ConversationAnalytics(chatbot.ai_client)
        sentiment_history = chatbot.get_sentiment_history()
        profile = analytics.generate_emotion_profile(sentiment_history)
        return jsonify({'profile': profile})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/report', methods=['GET'])
def get_report():
    """Get full analytics report."""
    try:
        session_id = session.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        analytics = ConversationAnalytics(chatbot.ai_client)
        report_gen = ReportGenerator(analytics)
        
        conversation_history = chatbot.get_history()
        sentiment_history = chatbot.get_sentiment_history()
        
        report = report_gen.generate_json_report(conversation_history, sentiment_history)
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reset', methods=['POST'])
def reset_chat():
    """Reset the conversation."""
    try:
        session_id = session.get('session_id', 'default')
        if session_id in chatbot_instances:
            chatbot_instances[session_id].reset()
        return jsonify({'status': 'success', 'message': 'Conversation reset'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/history', methods=['GET'])
def get_history():
    """Get conversation history."""
    try:
        session_id = session.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        history = chatbot.get_history()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🤖 AI Chatbot Web Interface")
    print("  Powered by Google Gemini Flash 2.5")
    print("="*60)
    print("\n  Open your browser and go to: http://127.0.0.1:5000")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
