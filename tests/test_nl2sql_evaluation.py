from app.llm.sql_generator import generate_sql


TEST_CASES = [
    {
        "question": "What was total booking in 2025Q1?",
        "expected_table": "actual_booking_invoices_collection",
        "expected_columns": ["booking_amount", "booking_week"],
        "expected_keywords": ["sum", "between", "2025wk01", "2025wk13"]
    },
    {
        "question": "What was total invoice in 2025Q2?",
        "expected_table": "actual_booking_invoices_collection",
        "expected_columns": ["invoice_amount", "invoice_week"],
        "expected_keywords": ["sum", "between", "2025wk14", "2025wk26"]
    },
    {
        "question": "What was collection in 2025Wk05?",
        "expected_table": "actual_booking_invoices_collection",
        "expected_columns": ["collection_amount", "collection_week"],
        "expected_keywords": ["2025wk05"]
    },
    {
        "question": "What is total forecasted invoice for 2025Q3?",
        "expected_table": "booking_to_invoice_forecasting",
        "expected_columns": ["forecasted_invoice", "booking_week"],
        "expected_keywords": ["sum", "2025wk27", "2025wk39"]
    },
    {
        "question": "What is forecasted collection for 2025Wk10?",
        "expected_table": "invoice_to_cash_forecasting",
        "expected_columns": ["forecasted_collection", "invoice_week"],
        "expected_keywords": ["2025wk10"]
    },
    {
        "question": "What percentage of booking is invoiced within 3 weeks?",
        "expected_table": "booking_to_invoice_forecasting",
        "expected_columns": ["lag_0", "lag_1", "lag_2", "lag_3"],
        "expected_keywords": ["avg"]
    }
]

def evaluate_sql(sql: str, test_case: dict):

    sql_lower = sql.lower()

    errors = []

    if test_case["expected_table"].lower() not in sql_lower:
        errors.append(
            f"Missing table: {test_case['expected_table']}"
        )

    for column in test_case["expected_columns"]:
        if column.lower() not in sql_lower:
            errors.append(
                f"Missing column: {column}"
            )

    for keyword in test_case["expected_keywords"]:
        if keyword.lower() not in sql_lower:
            errors.append(
                f"Missing keyword/value: {keyword}"
            )

    return errors

def run_evaluation():

    passed = 0
    failed = 0

    for i, test_case in enumerate(TEST_CASES, start=1):

        question = test_case["question"]

        print("\n" + "=" * 70)
        print(f"Test {i}")
        print("Question:", question)

        result = generate_sql(question)

        sql = result.sql

        print("\nGenerated SQL:")
        print(sql)

        errors = evaluate_sql(
            sql=sql,
            test_case=test_case
        )

        if not errors:
            print("\nRESULT: PASS")
            passed += 1

        else:
            print("\nRESULT: FAIL")

            for error in errors:
                print("-", error)

            failed += 1

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print("Total:", len(TEST_CASES))
    print("Passed:", passed)
    print("Failed:", failed)
    accuracy = (
    passed / len(TEST_CASES) * 100
    )

    print(f"Accuracy: {accuracy:.2f}%")


if __name__ == "__main__":
    run_evaluation()