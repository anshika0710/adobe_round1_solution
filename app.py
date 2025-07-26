from flask import Flask, request, jsonify
from graphene import ObjectType, String, List, Int, Schema

import json
import os

# Load JSON file (Round 1A output)
def load_pdf_data():
    path = os.path.join("output", "sample.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

pdf_data = load_pdf_data()

# Define GraphQL types
class HeadingType(ObjectType):
    level = String()
    text = String()
    page = Int()

class Query(ObjectType):
    title = String()
    outline = List(HeadingType)

    def resolve_title(parent, info):
        return pdf_data.get("title", "")

    def resolve_outline(parent, info):
        return pdf_data.get("outline", [])

schema = Schema(query=Query)

# Set up Flask app
app = Flask(__name__)

@app.route("/graphql", methods=["POST"])
def graphql_api():
    data = request.get_json()
    result = schema.execute(data.get("query"))
    return jsonify(result.data)



if __name__ == "__main__":
    app.run(debug=True)
