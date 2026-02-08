# COREP Assistant - Using Groq 
# Internship Project

from flask import Flask, render_template_string, request, jsonify
import os
from dotenv import load_dotenv
from template_generator import generate_corep_template, validate_fields
import json
from groq import Groq

# Load environment variables
load_dotenv()

# Check if API key exists
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    print("ERROR: Please add your GROQ_API_KEY to the .env file")
    print("Get a free key from: https://console.groq.com")
    exit(1)

# Create Groq client
client = Groq(api_key=groq_api_key)

app = Flask(__name__)
query_count = 0

def load_rules():
    """Load regulatory rules from file"""
    try:
        with open('rules.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("ERROR: rules.txt file not found!")
        return "No rules available"

def find_relevant_rules(question, all_rules):
    """Basic keyword matching"""
    question_lower = question.lower()
    keywords = ['cet1', 'tier 1', 'capital', 'deduction', 'own funds']
    
    if any(keyword in question_lower for keyword in keywords):
        return all_rules
    else:
        return all_rules

def process_with_groq(question, rules):
    """
    Improved version - gives different responses based on question type
    """
    
    
    prompt = f"""You are a UK banking regulatory compliance expert specializing in PRA COREP reporting.

REGULATORY RULES AVAILABLE:
{rules}

USER'S SPECIFIC QUESTION:
"{question}"

TASK: Carefully analyze the user's question and provide a customized response.

IMPORTANT INSTRUCTIONS:
1. If the user asks "how to calculate" something - explain the formula and components step by step
2. If the user asks "what are deductions" - list all deduction items specifically
3. If the user provides SPECIFIC NUMBERS (like £100M, £20M) - USE THOSE EXACT NUMBERS in calculations and show the math
4. If the user asks "what fields are required" - list the specific COREP form fields
5. Match your response DIRECTLY to what they asked - don't give generic answers

RESPONSE FORMAT (JSON):
{{
    "applicable_rules": ["list specific rule numbers/names that answer THIS question"],
    "required_fields": [
        {{
            "field_name": "exact field name from COREP or calculation",
            "value": "if user gave numbers USE THEM, otherwise say 'User to provide'",
            "rule_reference": "specific rule excerpt explaining THIS field"
        }}
    ],
    "validation_notes": "specific warnings or notes relevant to THIS question",
    "audit_trail": "detailed explanation of how you answered THIS SPECIFIC question"
}}

Now respond to the user's question: "{question}"
"""
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a precise regulatory expert. Tailor each response specifically to the user's question. Use exact numbers if provided. Give different answers for different questions."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        result = chat_completion.choices[0].message.content
        
        print(f"\n=== Question: {question[:50]}... ===")
        print(f"Response preview: {result[:200]}...")
        
        parsed = json.loads(result)
        
        if not all(key in parsed for key in ["applicable_rules", "required_fields", "validation_notes", "audit_trail"]):
            raise ValueError("Missing required fields in response")
        
        return json.dumps(parsed)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return create_fallback_response(question)


def create_fallback_response(question):
    """Create different fallback responses based on question type"""
    question_lower = question.lower()
    
    if "calculate" in question_lower or "how do i" in question_lower:
        return json.dumps({
            "applicable_rules": ["RULE 1: CET1 Calculation", "RULE 2: Deductions"],
            "required_fields": [
                {
                    "field_name": "Step 1: Add Capital Instruments (Ordinary Shares)",
                    "value": "Enter your bank's ordinary share capital",
                    "rule_reference": "RULE 1: CET1 capital consists of capital instruments"
                },
                {
                    "field_name": "Step 2: Add Share Premium",
                    "value": "Enter share premium amount",
                    "rule_reference": "RULE 1: Include share premium accounts"
                },
                {
                    "field_name": "Step 3: Add Retained Earnings",
                    "value": "Enter retained earnings",
                    "rule_reference": "RULE 1: Include retained earnings"
                },
                {
                    "field_name": "Step 4: Subtract Intangible Assets",
                    "value": "Enter intangibles as negative number",
                    "rule_reference": "RULE 2: Deduct intangible assets from CET1"
                },
                {
                    "field_name": "Final CET1 Capital",
                    "value": "Sum of all above items",
                    "rule_reference": "CET1 = Positive items - Deductions"
                }
            ],
            "validation_notes": "This is the step-by-step calculation process for CET1 capital",
            "audit_trail": f"Question asked: '{question}'. Provided step-by-step CET1 calculation methodology per PRA rules."
        })
    
    elif "deduction" in question_lower or "subtract" in question_lower:
        return json.dumps({
            "applicable_rules": ["RULE 2: Deductions from CET1"],
            "required_fields": [
                {
                    "field_name": "Intangible Assets (deduct)",
                    "value": "Enter as negative amount",
                    "rule_reference": "RULE 2: Intangible assets shall be deducted from CET1 items"
                },
                {
                    "field_name": "Deferred Tax Assets (deduct)",
                    "value": "Enter as negative amount",
                    "rule_reference": "RULE 2: Deferred tax assets that rely on future profitability shall be deducted"
                },
                {
                    "field_name": "Current Year Losses (deduct)",
                    "value": "Enter losses as negative amount",
                    "rule_reference": "RULE 2: Losses for the current financial year shall be deducted"
                }
            ],
            "validation_notes": "All deduction items should be entered as negative numbers or will reduce your CET1 capital",
            "audit_trail": f"Question asked: '{question}'. Listed all mandatory deductions from CET1 per PRA RULE 2."
        })
    
    elif "£" in question or any(char.isdigit() for char in question):
        # Question contains numbers - do calculation
        import re
        numbers = re.findall(r'£?(\d+)M?', question)
        
        shares = int(numbers[0]) * 1000 if len(numbers) > 0 else 0
        retained = int(numbers[1]) * 1000 if len(numbers) > 1 else 0
        intangibles = int(numbers[2]) * 1000 if len(numbers) > 2 else 0
        
        cet1_total = shares + retained - intangibles
        
        return json.dumps({
            "applicable_rules": ["RULE 1: CET1 Components", "RULE 2: Deductions"],
            "required_fields": [
                {
                    "field_name": "Ordinary Shares",
                    "value": f"{shares}",
                    "rule_reference": "RULE 1: Capital instruments eligible as CET1"
                },
                {
                    "field_name": "Retained Earnings",
                    "value": f"{retained}",
                    "rule_reference": "RULE 1: Retained earnings included in CET1"
                },
                {
                    "field_name": "Intangible Assets (deduction)",
                    "value": f"-{intangibles}",
                    "rule_reference": "RULE 2: Intangible assets deducted from CET1"
                },
                {
                    "field_name": "TOTAL Common Equity Tier 1 Capital",
                    "value": f"{cet1_total}",
                    "rule_reference": "Calculated as: Shares + Retained Earnings - Intangibles"
                }
            ],
            "validation_notes": f"Based on your numbers: £{shares//1000}M + £{retained//1000}M - £{intangibles//1000}M = £{cet1_total//1000}M CET1",
            "audit_trail": f"Question: '{question}'. Extracted values and calculated CET1 = {shares} + {retained} - {intangibles} = {cet1_total} (thousands)"
        })
    
    else:
        return json.dumps({
            "applicable_rules": ["RULE 1: CET1 Definition"],
            "required_fields": [
                {
                    "field_name": "Common Equity Tier 1 Capital",
                    "value": "To be calculated",
                    "rule_reference": "RULE 1: CET1 consists of capital instruments, share premium, retained earnings, reserves"
                }
            ],
            "validation_notes": "Please provide more specific details for a tailored response",
            "audit_trail": f"Question: '{question}'. General CET1 information provided."
        })

@app.route('/')
def home():
    """Main page"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>COREP Assistant - Groq Powered</title>
        <meta charset="UTF-8">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 28px;
                margin-bottom: 10px;
            }
            
            .header p {
                opacity: 0.9;
                font-size: 14px;
            }
            
            .groq-badge {
                display: inline-block;
                background: rgba(255,255,255,0.2);
                padding: 5px 15px;
                border-radius: 20px;
                margin-top: 10px;
                font-size: 12px;
            }
            
            .content {
                padding: 30px;
            }
            
            .info-box {
                background: #e3f2fd;
                border-left: 4px solid #2196f3;
                padding: 15px;
                margin-bottom: 25px;
                border-radius: 5px;
            }
            
            .info-box h3 {
                color: #1976d2;
                margin-bottom: 10px;
                font-size: 16px;
            }
            
            .info-box ul {
                margin-left: 20px;
                color: #555;
                font-size: 14px;
                line-height: 1.8;
            }
            
            .input-section {
                margin-bottom: 20px;
            }
            
            .input-section label {
                display: block;
                font-weight: 600;
                margin-bottom: 10px;
                color: #333;
            }
            
            textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 15px;
                font-family: inherit;
                resize: vertical;
                transition: border-color 0.3s;
            }
            
            textarea:focus {
                outline: none;
                border-color: #f5576c;
            }
            
            .button-group {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            
            button {
                flex: 1;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(245, 87, 108, 0.4);
            }
            
            button:active {
                transform: translateY(0);
            }
            
            .clear-btn {
                background: #6c757d;
                flex: 0.3;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
                color: #f5576c;
                font-style: italic;
            }
            
            .loading::after {
                content: '...';
                animation: dots 1.5s steps(4, end) infinite;
            }
            
            @keyframes dots {
                0%, 20% { content: '.'; }
                40% { content: '..'; }
                60%, 100% { content: '...'; }
            }
            
            #result {
                margin-top: 30px;
            }
            
            .footer {
                text-align: center;
                padding: 20px;
                background: #f8f9fa;
                color: #666;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>COREP Regulatory Reporting Assistant</h1>
                <p>AI-Powered Prototype for PRA COREP Compliance | Internship Project 2026</p>
                <div class="groq-badge">⚡ Powered by Groq + Llama 3.3 70B</div>
            </div>
            
            <div class="content">
                <div class="info-box">
                    <h3>💡 Try These Example Questions:</h3>
                    <ul>
                        <li>"How do I calculate Common Equity Tier 1 capital?"</li>
                        <li>"What are the deductions from CET1?"</li>
                        <li>"Our bank has £100M ordinary shares, £20M retained earnings, and £5M intangibles. Calculate CET1."</li>
                        <li>"What fields are required for Own Funds COREP reporting?"</li>
                    </ul>
                </div>
                
                <div class="input-section">
                    <label for="question">Enter Your Regulatory Reporting Question:</label>
                    <textarea 
                        id="question" 
                        rows="5" 
                        placeholder="Describe your reporting scenario or ask a question about COREP requirements..."
                    ></textarea>
                </div>
                
                <div class="button-group">
                    <button onclick="askQuestion()">Get AI Assistance</button>
                    <button class="clear-btn" onclick="clearAll()">Clear</button>
                </div>
                
                <div class="loading" id="loading">
                    🤖 Processing with Groq AI
                </div>
                
                <div id="result"></div>
            </div>
            
            <div class="footer">
                Built with Flask + Groq (Llama 3.3 70B) 
            </div>
        </div>
        
        <script>
            let queryCount = 0;
            
            async function askQuestion() {
                const question = document.getElementById('question').value;
                const resultDiv = document.getElementById('result');
                const loadingDiv = document.getElementById('loading');
                
                if (!question.trim()) {
                    alert('Please enter a question first!');
                    return;
                }
                
                loadingDiv.style.display = 'block';
                resultDiv.innerHTML = '';
                
                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({question: question})
                    });
                    
                    const data = await response.json();
                    queryCount++;
                    
                    resultDiv.innerHTML = data.formatted_output;
                    
                } catch (error) {
                    resultDiv.innerHTML = `
                        <div style='padding: 20px; background: #f8d7da; border-left: 4px solid #dc3545; border-radius: 5px;'>
                            <h4 style='color: #721c24; margin-bottom: 10px;'>❌ Error</h4>
                            <p style='color: #721c24;'>${error.message}</p>
                        </div>
                    `;
                } finally {
                    loadingDiv.style.display = 'none';
                }
            }
            
            function clearAll() {
                document.getElementById('question').value = '';
                document.getElementById('result').innerHTML = '';
            }
            
            document.getElementById('question').addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && e.ctrlKey) {
                    askQuestion();
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/ask', methods=['POST'])
def ask():
    """Main API endpoint"""
    global query_count
    query_count += 1
    
    data = request.json
    question = data.get('question', '')
    
    print(f"\n--- Query #{query_count} (Groq) ---")
    print(f"Question: {question}")
    
    all_rules = load_rules()
    relevant_rules = find_relevant_rules(question, all_rules)
    print("Rules loaded ✓")
    
    llm_response = process_with_groq(question, relevant_rules)
    print("Groq processing complete ✓")
    
    formatted_output = generate_corep_template(llm_response)
    print("Template generated ✓")
    
    try:
        response_data = json.loads(llm_response)
        validation_errors = validate_fields(response_data.get('required_fields', []))
        
        if validation_errors:
            formatted_output += """
            <div style='margin-top: 20px; padding: 15px; background-color: #f8d7da; border-left: 4px solid #dc3545; border-radius: 5px;'>
                <h4 style='margin-top: 0; color: #721c24;'>⚠️ Additional Validation Warnings:</h4>
                <ul style='margin-left: 20px; color: #721c24;'>
            """
            for error in validation_errors:
                formatted_output += f"<li>{error}</li>"
            formatted_output += "</ul></div>"
    except:
        pass
    
    return jsonify({
        'response': llm_response,
        'formatted_output': formatted_output,
        'query_number': query_count
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🏦 COREP Assistant Starting (Groq Version)...")
    print("="*50)
    print("📍 Server: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)