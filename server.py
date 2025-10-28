from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_html():
    """Receive HTML content and save it to a file"""
    html_content = request.data.decode('utf-8')

    # Save to output directory
    output_dir = 'received_reports'
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename with timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(output_dir, f'report_{timestamp}.html')

    with open(output_path, 'w') as f:
        f.write(html_content)

    print(f"Received HTML report and saved to {output_path}")
    return {'status': 'success', 'file': output_path}, 200

if __name__ == '__main__':
    print("Starting server on http://localhost:3000")
    print("Ready to receive HTML reports...")
    app.run(host='0.0.0.0', port=3000, debug=True)
