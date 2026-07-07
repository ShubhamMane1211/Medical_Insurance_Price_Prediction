from app import app as application

if __name__ == "__main__":
    print("=" * 50)
    print("Starting Flask Server...")
    print("Local URL: http://127.0.0.1:5000")
    print("Network URL: http://0.0.0.0:5000")
    print("=" * 50)

    application.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,
    )
