@app.route("/api/add/store",methods=["POST"])
@token_required
def store(user):
    if request.method == "POST":
        return add