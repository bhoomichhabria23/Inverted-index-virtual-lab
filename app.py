import os
import re
from datetime import datetime

import pandas as pd
import streamlit as st
from fpdf import FPDF


# 1. EXPERIMENT CONFIGURATION

EXPERIMENT_CONFIG = {
    "title": "Construction of an Inverted Index",
    "brief": (
        "Create an inverted index mapping terms to documents and their occurrences. "
        "The experiment demonstrates how search engines organize terms so that "
        "documents containing a particular keyword can be retrieved efficiently."
    ),
    "expected_outcome": (
        "A basic searchable index supporting efficient keyword retrieval."
    ),
    "objectives": [
        "Understand the concept and structure of an inverted index.",
        "Tokenize documents into individual terms.",
        "Map each term to the documents in which it occurs.",
        "Record the occurrence frequency of each term in each document.",
        "Perform keyword searches using the constructed inverted index.",
        "Observe how an inverted index supports efficient document retrieval."
    ]
}


# 2. THEORY CONTENT

THEORY_CONTENT = {
    "background": """
### Inverted Index

An **inverted index** is a data structure commonly used in information retrieval
systems and search engines. Instead of storing documents and then scanning every
document for a search term, the inverted index stores a mapping from each term
to the documents where that term occurs.

### Example

Suppose we have three documents:

- **D1:** apple banana orange
- **D2:** banana mango apple
- **D3:** orange mango banana

The inverted index contains:

| Term | Posting List |
|---|---|
| apple | D1(1), D2(1) |
| banana | D1(1), D2(1), D3(1) |
| mango | D2(1), D3(1) |
| orange | D1(1), D3(1) |

The number inside brackets represents the number of occurrences of that term
in the document.

### Why is it called an "inverted" index?

A normal document collection can be viewed as:

**Document → Terms**

An inverted index reverses this relationship:

**Term → Documents**

Therefore, it is called an **inverted index**.

### Basic Workflow

1. Collect a set of documents.
2. Tokenize each document into terms.
3. Normalize the terms.
4. Count term occurrences.
5. Create a mapping from each term to its documents.
6. Store the posting list.
7. Search the index using a keyword.
8. Return documents containing that keyword.

### Search Process

If the user searches for **banana**, the system does not need to scan all
documents individually. It directly accesses the posting list of `banana`.

For the example above:

**banana → D1, D2, D3**

This demonstrates efficient keyword retrieval.

### Important Components

**Term:** An individual word extracted from a document.

**Document:** A text item identified using a document ID.

**Posting:** Information showing that a term occurs in a particular document.

**Posting List:** The list of documents associated with a particular term.

**Term Frequency:** Number of times a term occurs in a document.

**Dictionary:** The collection of unique terms in the index.
""",

    "procedure": [
        "Step 1: Study the concept of an inverted index and posting lists.",
        "Step 2: Enter or use the sample collection of documents.",
        "Step 3: Tokenize each document into individual terms.",
        "Step 4: Convert terms to lowercase and remove unnecessary punctuation.",
        "Step 5: Count the occurrence of every term in each document.",
        "Step 6: Construct the inverted index by mapping every term to its postings.",
        "Step 7: Observe the generated term dictionary and posting lists.",
        "Step 8: Enter a keyword in the search box.",
        "Step 9: Retrieve the documents containing the searched keyword.",
        "Step 10: Record the trial and observe the retrieval results.",
        "Step 11: Complete the conceptual quiz.",
        "Step 12: Generate and download the experiment report."
    ],

    "key_terms": {
        "Document": "A text item used as input for index construction.",
        "Term": "An individual word extracted from a document.",
        "Tokenization": "Process of splitting document text into individual terms.",
        "Inverted Index": "A mapping from terms to documents containing those terms.",
        "Posting": "A record connecting a term with a document and its occurrence count.",
        "Posting List": "Collection of postings associated with a term.",
        "Term Frequency": "Number of times a term occurs in a document.",
        "Keyword Retrieval": "Finding documents that contain a searched term."
    }
}


# 3. INDEX CONSTRUCTION ENGINE

def tokenize(text):
    """
    Converts text into normalized terms.
    """
    text = text.lower()
    return re.findall(r"\b[a-z0-9]+\b", text)


def build_inverted_index(documents):
    """
    Constructs an inverted index.

    Format:
    {
        term: {
            document_id: occurrence_count
        }
    }
    """

    index = {}

    for doc_id, text in documents.items():
        tokens = tokenize(text)

        for token in tokens:
            if token not in index:
                index[token] = {}

            if doc_id not in index[token]:
                index[token][doc_id] = 0

            index[token][doc_id] += 1

    return dict(sorted(index.items()))


def search_index(index, query):
    """
    Searches the inverted index for a keyword.
    """

    query_terms = tokenize(query)

    if not query_terms:
        return {}

    results = {}

    for term in query_terms:
        if term in index:
            results[term] = index[term]

    return results


def create_index_dataframe(index):
    """
    Converts inverted index into a DataFrame for display.
    """

    rows = []

    for term, postings in index.items():
        posting_text = ", ".join(
            f"{doc_id} ({count})"
            for doc_id, count in postings.items()
        )

        total_occurrences = sum(postings.values())

        rows.append({
            "Term": term,
            "Posting List": posting_text,
            "Documents": len(postings),
            "Total Occurrences": total_occurrences
        })

    return pd.DataFrame(rows)


# 4. QUIZ

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the main purpose of an inverted index?",
        "options": [
            "A) Store images only",
            "B) Map terms to documents containing those terms",
            "C) Delete duplicate documents",
            "D) Encrypt documents"
        ],
        "answer_index": 1,
        "explanation": (
            "An inverted index maps each term to the documents in which "
            "that term occurs."
        )
    },
    {
        "id": 2,
        "question": "Why is the index called an 'inverted' index?",
        "options": [
            "A) It reverses the letters of every word",
            "B) It reverses the order of documents",
            "C) It changes the relationship from Document → Terms to Term → Documents",
            "D) It stores documents upside down"
        ],
        "answer_index": 2,
        "explanation": (
            "The relationship is inverted from documents pointing to terms "
            "to terms pointing to documents."
        )
    },
    {
        "id": 3,
        "question": "What is a posting list?",
        "options": [
            "A) A list of all users",
            "B) A list of documents associated with a term",
            "C) A list of search engines",
            "D) A list of programming languages"
        ],
        "answer_index": 1,
        "explanation": (
            "A posting list contains information about documents in which "
            "a particular term occurs."
        )
    },
    {
        "id": 4,
        "question": "What does term frequency represent?",
        "options": [
            "A) Number of documents in the system",
            "B) Number of different users",
            "C) Number of times a term occurs in a document",
            "D) Number of searches performed"
        ],
        "answer_index": 2,
        "explanation": (
            "Term frequency is the number of occurrences of a term "
            "within a particular document."
        )
    },
    {
        "id": 5,
        "question": "What is tokenization?",
        "options": [
            "A) Splitting text into individual terms",
            "B) Encrypting the document",
            "C) Deleting the index",
            "D) Sorting documents by size"
        ],
        "answer_index": 0,
        "explanation": (
            "Tokenization divides a document into individual words or terms."
        )
    },
    {
        "id": 6,
        "question": "If 'apple' occurs twice in D1, what should the posting contain?",
        "options": [
            "A) D1 (2)",
            "B) D1 (0)",
            "C) D2 (2)",
            "D) apple (0)"
        ],
        "answer_index": 0,
        "explanation": (
            "The posting records document D1 and the occurrence count of 2."
        )
    },
    {
        "id": 7,
        "question": "What happens when a user searches for a term present in the index?",
        "options": [
            "A) Every document must always be deleted",
            "B) The posting list for that term can be retrieved",
            "C) The index is rebuilt automatically",
            "D) The search is ignored"
        ],
        "answer_index": 1,
        "explanation": (
            "The system accesses the posting list associated with the searched term."
        )
    },
    {
        "id": 8,
        "question": "Which of the following is a unique term?",
        "options": [
            "A) A repeated occurrence of the same word",
            "B) A distinct word appearing in the document collection",
            "C) A document ID",
            "D) A posting count"
        ],
        "answer_index": 1,
        "explanation": (
            "A unique term represents one distinct word in the indexed collection."
        )
    },
    {
        "id": 9,
        "question": "What is the main benefit of using an inverted index for keyword search?",
        "options": [
            "A) It makes every document longer",
            "B) It avoids storing any terms",
            "C) It allows direct access to documents associated with a term",
            "D) It removes all search queries"
        ],
        "answer_index": 2,
        "explanation": (
            "The index provides a direct mapping from a keyword to its associated documents."
        )
    },
    {
        "id": 10,
        "question": "Which relationship represents an inverted index?",
        "options": [
            "A) Document → Terms",
            "B) Term → Documents",
            "C) User → Password",
            "D) Document → Image"
        ],
        "answer_index": 1,
        "explanation": (
            "An inverted index represents the Term → Documents relationship."
        )
    }
]

PRETEST_QUESTIONS = QUIZ_QUESTIONS[:5]
POSTTEST_QUESTIONS = QUIZ_QUESTIONS[5:]


# 5. PDF REPORT

class LabReportPDF(FPDF):

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)

        self.cell(
            0,
            10,
            f"Page {self.page_no()}/{{nb}} | Virtual Laboratory Report",
            align="C"
        )


def generate_pdf_report(
    student_name,
    student_id,
    date_str,
    documents,
    index_df,
    search_history,
    pretest_score,
    posttest_score,
    student_notes
):

    pdf = LabReportPDF()

    pdf.alias_nb_pages()

    pdf.set_auto_page_break(
        auto=True,
        margin=18
    )

    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(15, 23, 42)

    pdf.cell(
        0,
        10,
        EXPERIMENT_CONFIG["title"],
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.ln(3)

    # Student Information
    pdf.set_font("Helvetica", "B", 10)

    pdf.cell(
        0,
        7,
        "Student Information",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 9)

    pdf.cell(
        0,
        5,
        f"Student Name: {student_name or 'N/A'}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0,
        5,
        f"Student Roll / ID: {student_id or 'N/A'}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0,
        5,
        f"Experiment Date: {date_str}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0,
        5,
        f"Pretest Score: {pretest_score} / {len(PRETEST_QUESTIONS)}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.cell(
        0,
        5,
        f"Posttest Score: {posttest_score} / {len(POSTTEST_QUESTIONS)}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.ln(6)

    # Objectives
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 58, 138)

    pdf.cell(
        0,
        7,
        "1. Learning Objectives",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)

    for objective in EXPERIMENT_CONFIG["objectives"]:

        pdf.multi_cell(
            0,
            5,
            "- " + objective,
            new_x="LMARGIN",
            new_y="NEXT"
        )

    pdf.ln(4)

    # Documents
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 58, 138)

    pdf.cell(
        0,
        7,
        "2. Input Documents",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)

    for doc_id, text in documents.items():

        pdf.multi_cell(
            0,
            5,
            f"{doc_id}: {text}",
            new_x="LMARGIN",
            new_y="NEXT"
        )

    pdf.ln(4)

    # Inverted Index
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 58, 138)

    pdf.cell(
        0,
        7,
        "3. Constructed Inverted Index",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    if index_df.empty:

        pdf.set_font("Helvetica", "I", 9)

        pdf.cell(
            0,
            6,
            "No index data available.",
            new_x="LMARGIN",
            new_y="NEXT"
        )

    else:

        pdf.set_font("Helvetica", "B", 8)

        cols = [
            "Term",
            "Posting List",
            "Documents",
            "Total Occurrences"
        ]

        widths = [30, 90, 30, 40]

        pdf.set_fill_color(37, 99, 235)
        pdf.set_text_color(255, 255, 255)

        for col, width in zip(cols, widths):

            pdf.cell(
                width,
                6,
                col,
                border=1,
                align="C",
                fill=True
            )

        pdf.ln()

        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(30, 41, 59)

        for _, row in index_df.iterrows():

            pdf.cell(
                widths[0],
                5,
                str(row["Term"])[:18],
                border=1,
                align="C"
            )

            pdf.cell(
                widths[1],
                5,
                str(row["Posting List"])[:45],
                border=1,
                align="C"
            )

            pdf.cell(
                widths[2],
                5,
                str(row["Documents"]),
                border=1,
                align="C"
            )

            pdf.cell(
                widths[3],
                5,
                str(row["Total Occurrences"]),
                border=1,
                align="C"
            )

            pdf.ln()

    pdf.ln(6)

    # Search History
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 58, 138)

    pdf.cell(
        0,
        7,
        "4. Keyword Retrieval Trials",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)

    if search_history:

        for trial in search_history:

            pdf.multi_cell(
                0,
                5,
                f"Query: {trial['Query']} | "
                f"Retrieved: {trial['Retrieved Documents']}",
                new_x="LMARGIN",
                new_y="NEXT"
            )

    else:

        pdf.cell(
            0,
            6,
            "No keyword search trials recorded.",
            new_x="LMARGIN",
            new_y="NEXT"
        )

    pdf.ln(5)

    # Observations
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 58, 138)

    pdf.cell(
        0,
        7,
        "5. Observations & Analysis",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)

    notes = student_notes.strip()

    if not notes:

        notes = (
            "The experiment successfully constructed an inverted index by "
            "mapping terms to documents and their occurrence counts. "
            "Keyword searches retrieved the corresponding documents using "
            "the generated posting lists."
        )

    pdf.multi_cell(
        0,
        5,
        notes,
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.ln(5)

    # Conclusion
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(30, 58, 138)

    pdf.cell(
        0,
        7,
        "6. Conclusion",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)

    pdf.multi_cell(
        0,
        5,
        "An inverted index was constructed successfully. "
        "The experiment demonstrated the mapping of terms to documents "
        "and their occurrence frequencies. The resulting index supported "
        "basic keyword retrieval without scanning every document individually.",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    return bytes(pdf.output())


# 6. THEORY SECTION

def render_aim_section():

    st.write(
        "Aim: To construct an inverted index that maps each term to the documents "
        "in which it occurs and use the index to perform efficient "
        "keyword-based information retrieval."
    )


def render_theory_section():

    st.header("Theory")

    st.markdown(
        THEORY_CONTENT["background"]
    )

    st.info(
        EXPERIMENT_CONFIG["brief"]
    )

    st.subheader("Learning Objectives")

    for i, objective in enumerate(EXPERIMENT_CONFIG["objectives"]):

        st.write(
            f"**Objective {i + 1}:** {objective}"
        )

    st.subheader("Expected Outcome")

    st.success(
        EXPERIMENT_CONFIG["expected_outcome"]
    )

    with st.expander("Key Terminology & Variable Reference"):

        terms_df = pd.DataFrame(
            list(THEORY_CONTENT["key_terms"].items()),
            columns=[
                "Term",
                "Definition"
            ]
        )

        st.table(terms_df)


def render_procedure_section():

    st.header("Experimental Procedure")

    for step in THEORY_CONTENT["procedure"]:

        st.write(
            f"- {step}"
        )


# 7. SIMULATION SECTION

def render_simulation_section():

    st.header("Interactive Inverted Index Construction")

    st.write(
        "Enter documents below, construct the inverted index, "
        "and then perform keyword retrieval."
    )

    st.subheader("Step 1: Enter Documents")

    col1, col2 = st.columns(2)

    with col1:

        doc1 = st.text_area(
            "Document D1",
            placeholder="Enter text for Document D1",
            height=100
        )

        doc2 = st.text_area(
            "Document D2",
            placeholder="Enter text for Document D2",
            height=100
        )

    with col2:

        doc3 = st.text_area(
            "Document D3",
            placeholder="Enter text for Document D3",
            height=100
        )

        doc4 = st.text_area(
            "Document D4",
            placeholder="Enter text for Document D4",
            height=100
        )

    documents = {
        "D1": doc1,
        "D2": doc2,
        "D3": doc3,
        "D4": doc4
    }

    st.divider()

    st.subheader("Step 2: Construct Inverted Index")

    if st.button(
        "Build Inverted Index",
        type="primary",
        use_container_width=True
    ):

        index = build_inverted_index(documents)

        st.session_state["current_documents"] = documents
        st.session_state["current_index"] = index

        st.success(
            f"Inverted index constructed successfully with "
            f"{len(index)} unique terms."
        )

    if "current_index" in st.session_state:

        index = st.session_state["current_index"]

        st.subheader("Generated Inverted Index")

        index_df = create_index_dataframe(index)

        st.dataframe(
            index_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # Statistics
        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Documents",
                len(st.session_state["current_documents"])
            )

        with col2:

            st.metric(
                "Unique Terms",
                len(index)
            )

        with col3:

            total_occurrences = sum(
                sum(postings.values())
                for postings in index.values()
            )

            st.metric(
                "Total Term Occurrences",
                total_occurrences
            )

        st.divider()

        # Search
        st.subheader("Step 3: Keyword Retrieval")

        query = st.text_input(
            "Enter a keyword to search",
            placeholder="Enter a keyword"
        )

        if st.button(
            "Search Index",
            use_container_width=True
        ):

            results = search_index(
                index,
                query
            )

            if results:

                retrieved_documents = set()

                for postings in results.values():

                    retrieved_documents.update(
                        postings.keys()
                    )

                retrieved_documents = sorted(
                    retrieved_documents
                )

                st.success(
                    f"Retrieved {len(retrieved_documents)} document(s): "
                    f"{', '.join(retrieved_documents)}"
                )

                for term, postings in results.items():

                    st.write(
                        f"**Term:** `{term}`"
                    )

                    result_rows = []

                    for doc_id, count in postings.items():

                        result_rows.append({
                            "Document": doc_id,
                            "Occurrences": count,
                            "Document Text":
                                st.session_state[
                                    "current_documents"
                                ][doc_id]
                        })

                    st.dataframe(
                        pd.DataFrame(result_rows),
                        use_container_width=True,
                        hide_index=True
                    )

                trial = {
                    "Trial #": len(
                        st.session_state["search_history"]
                    ) + 1,
                    "Query": query,
                    "Retrieved Documents":
                        ", ".join(retrieved_documents),
                    "Number of Documents":
                        len(retrieved_documents),
                    "Timestamp":
                        datetime.now().strftime("%H:%M:%S")
                }

                st.session_state[
                    "search_history"
                ].append(trial)

            else:

                st.warning(
                    f"No document contains the keyword "
                    f"'{query}'."
                )

        st.divider()

        st.subheader("Keyword Search Trial Log")

        if st.session_state["search_history"]:

            history_df = pd.DataFrame(
                st.session_state["search_history"]
            )

            st.dataframe(
                history_df,
                use_container_width=True,
                hide_index=True
            )

            csv_data = history_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "Download Search Trials as CSV",
                data=csv_data,
                file_name="inverted_index_trials.csv",
                mime="text/csv",
                use_container_width=True
            )

        else:

            st.info(
                "No keyword retrieval trials recorded yet."
            )

        if st.button(
            "Clear Search Trial Log",
            use_container_width=True
        ):

            st.session_state["search_history"] = []

            st.rerun()


# 8. QUIZ SECTION

def render_quiz_section(quiz_type, questions):

    quiz_key = quiz_type.lower()
    answers_key = f"{quiz_key}_answers"
    submitted_key = f"{quiz_key}_submitted"
    score_key = f"{quiz_key}_score"

    st.header(f"{quiz_type} Quiz")

    st.write(
        "Answer the questions to test your understanding "
        "of inverted index construction and keyword retrieval."
    )

    with st.form(f"inverted_index_{quiz_key}_quiz"):

        user_responses = {}

        for question_number, question in enumerate(questions, start=1):

            st.subheader(
                f"Question {question_number}"
            )

            st.write(
                question["question"]
            )

            selected = st.radio(
                f"Options for Question {question_number}",
                question["options"],
                index=None,
                key=f"{quiz_key}_quiz_{question['id']}",
                label_visibility="collapsed"
            )

            user_responses[
                question["id"]
            ] = (
                question["options"].index(selected)
                if selected is not None
                else None
            )

        submitted = st.form_submit_button(
            "Submit Quiz for Grading",
            type="primary"
        )

    if submitted:

        unanswered_questions = [
            question_id
            for question_id, answer in user_responses.items()
            if answer is None
        ]

        if unanswered_questions:

            st.warning(
                "Please select an answer for every question before submitting."
            )

            return

        score = 0

        st.session_state[
            answers_key
        ] = user_responses

        st.session_state[
            submitted_key
        ] = True

        st.divider()

        st.subheader(
            "Evaluation Results"
        )

        for question_number, question in enumerate(questions, start=1):

            user_answer = user_responses[
                question["id"]
            ]

            correct_answer = question[
                "answer_index"
            ]

            if user_answer == correct_answer:

                score += 1

                st.success(
                    f"Question {question_number}: Correct!"
                )

                st.write(
                    question["explanation"]
                )

            else:

                st.error(
                    f"Question {question_number}: Incorrect."
                )

                st.write(
                    f"Correct Answer: "
                    f"{question['options'][correct_answer]}"
                )

                st.write(
                    question["explanation"]
                )

        st.session_state[
            score_key
        ] = score

        percentage = (
            score / len(questions)
        ) * 100

        st.info(
            f"Final Score: **{score} / "
            f"{len(questions)}** "
            f"({percentage:.0f}%)"
        )

    elif st.session_state.get(
        submitted_key,
        False
    ):

        st.success(
            f"{quiz_type} already submitted. "
            f"Current score: "
            f"**{st.session_state.get(score_key, 0)} / "
            f"{len(questions)}**"
        )


# 9. REPORT SECTION

def render_report_section():

    st.header("Report Generation")

    st.write(
        "Enter your details and generate a PDF report "
        "containing the experiment results."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        student_name = st.text_input(
            "Student Name",
            value=st.session_state[
                "student_info"
            ].get(
                "name",
                ""
            )
        )

    with col2:

        student_id = st.text_input(
            "Student Roll / ID",
            value=st.session_state[
                "student_info"
            ].get(
                "id",
                ""
            )
        )

    with col3:

        lab_date = st.date_input(
            "Experiment Date",
            value=datetime.now()
        )

    st.session_state[
        "student_info"
    ] = {
        "name": student_name,
        "id": student_id,
        "date": str(lab_date)
    }

    st.subheader(
        "Observations & Analysis"
    )

    student_notes = st.text_area(
        "Enter your observations and conclusion:",
        value=st.session_state.get(
            "student_notes",
            ""
        ),
        height=150
    )

    st.session_state[
        "student_notes"
    ] = student_notes

    st.divider()

    st.subheader(
        "Report Summary Preview"
    )

    st.write(
        f"**Experiment:** "
        f"{EXPERIMENT_CONFIG['title']}"
    )

    st.write(
        f"**Student:** {student_name}"
    )

    st.write(
        f"**Student ID:** {student_id}"
    )

    st.write(
        f"**Date:** {lab_date}"
    )

    st.write(
        f"**Pretest Score:** "
        f"{st.session_state.get('pretest_score', 0)} / "
        f"{len(PRETEST_QUESTIONS)}"
    )

    st.write(
        f"**Posttest Score:** "
        f"{st.session_state.get('posttest_score', 0)} / "
        f"{len(POSTTEST_QUESTIONS)}"
    )

    if "current_index" in st.session_state:

        index_df = create_index_dataframe(
            st.session_state["current_index"]
        )

        st.subheader(
            "Constructed Inverted Index"
        )

        st.dataframe(
            index_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        index_df = pd.DataFrame()

        st.info(
            "Build the inverted index from the "
            "Simulation section before generating the report."
        )

    search_history = st.session_state[
        "search_history"
    ]

    pdf_bytes = generate_pdf_report(
        student_name=student_name,
        student_id=student_id,
        date_str=str(lab_date),
        documents=st.session_state.get(
            "current_documents",
            {}
        ),
        index_df=index_df,
        search_history=search_history,
        pretest_score=st.session_state.get(
            "pretest_score",
            0
        ),
        posttest_score=st.session_state.get(
            "posttest_score",
            0
        ),
        student_notes=student_notes
    )

    st.divider()

    st.subheader(
        "Download Official Lab Report"
    )

    st.download_button(
        label="Download Lab Report (.pdf)",
        data=pdf_bytes,
        file_name="inverted_index_lab_report.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )


# 10. SESSION STATE

def init_session_state():

    if "search_history" not in st.session_state:

        st.session_state[
            "search_history"
        ] = []

    if "pretest_answers" not in st.session_state:

        st.session_state[
            "pretest_answers"
        ] = {}

    if "pretest_submitted" not in st.session_state:

        st.session_state[
            "pretest_submitted"
        ] = False

    if "pretest_score" not in st.session_state:

        st.session_state[
            "pretest_score"
        ] = 0

    if "posttest_answers" not in st.session_state:

        st.session_state[
            "posttest_answers"
        ] = {}

    if "posttest_submitted" not in st.session_state:

        st.session_state[
            "posttest_submitted"
        ] = False

    if "posttest_score" not in st.session_state:

        st.session_state[
            "posttest_score"
        ] = 0

    if "student_info" not in st.session_state:

        st.session_state[
            "student_info"
        ] = {
            "name": "",
            "id": "",
            "date": str(
                datetime.now().date()
            )
        }

    if "student_notes" not in st.session_state:

        st.session_state[
            "student_notes"
        ] = ""


# 11. MAIN ENTRY POINT

def main():

    st.set_page_config(
        page_title="Construction of an Inverted Index",
        page_icon="",
        layout="wide"
    )

    init_session_state()

    st.title(
        EXPERIMENT_CONFIG["title"]
    )

    st.caption(
        "Information Retrieval | Virtual Laboratory"
    )

    section = st.sidebar.radio(
        "Lab Navigator",
        [
            "Aim",
            "Theory",
            "Procedure",
            "Simulation",
            "Pretest",
            "Posttest",
            "Report Generation"
        ]
    )

    st.sidebar.divider()

    st.sidebar.subheader(
        "Experiment Progress"
    )

    if "current_index" in st.session_state:

        st.sidebar.write(
            "Index Construction: **Completed**"
        )

    else:

        st.sidebar.write(
            "Index Construction: **Pending**"
        )

    if st.session_state.get(
        "search_history"
    ):

        st.sidebar.write(
            f"Search Trials: "
            f"**{len(st.session_state['search_history'])}**"
        )

    else:

        st.sidebar.write(
            "Search Trials: **0**"
        )

    if st.session_state.get("pretest_submitted"):

        st.sidebar.write(
            "Pretest: **Completed**"
        )

        st.sidebar.write(
            f"Score: "
            f"**{st.session_state.get('pretest_score', 0)} / "
            f"{len(PRETEST_QUESTIONS)}**"
        )

    else:

        st.sidebar.write(
            "Pretest: **Pending**"
        )

    if st.session_state.get("posttest_submitted"):

        st.sidebar.write(
            "Posttest: **Completed**"
        )

        st.sidebar.write(
            f"Score: "
            f"**{st.session_state.get('posttest_score', 0)} / "
            f"{len(POSTTEST_QUESTIONS)}**"
        )

    else:

        st.sidebar.write(
            "Posttest: **Pending**"
        )

    if section == "Aim":

        render_aim_section()

    elif section == "Theory":

        render_theory_section()

    elif section == "Procedure":

        render_procedure_section()

    elif section == "Simulation":

        render_simulation_section()

    elif section == "Pretest":

        render_quiz_section("Pretest", PRETEST_QUESTIONS)

    elif section == "Posttest":

        render_quiz_section("Posttest", POSTTEST_QUESTIONS)

    elif section == "Report Generation":

        render_report_section()


if __name__ == "__main__":

    main()