import json
import os
from app.llm.sql_generator import generate_sql
from app.services.query_service import execute_safe_query


TEST_CASES_PATH = "evaluation/test_cases.json"


def load_test_cases():

    with open(
        TEST_CASES_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def normalize_result(result: list[dict]) -> list[dict]:

    normalized = []

    for row in result:

        normalized_row = {}

        for key, value in row.items():

            if isinstance(value, float):
                normalized_row[key] = round(value, 2)

            else:
                normalized_row[key] = value

        normalized.append(
            normalized_row
        )

    return normalized


def run_evaluation():

    test_cases = load_test_cases()

    results = []

    for test_case in test_cases:

        question = test_case["question"]

        print("\n" + "=" * 70)
        print(
            f"Test {test_case['id']}: {question}"
        )

        try:

            generated = generate_sql(
                question=question
            )

            generated_result = execute_safe_query(
                generated.sql
            )

            expected_result = execute_safe_query(
                test_case["expected_sql"]
            )

            query_type_pass = (
                generated.query_type
                == test_case["expected_query_type"]
            )

            response_type_pass = (
                generated.response_type
                == test_case["expected_response_type"]
            )

            result_pass = (
                normalize_result(generated_result)
                ==
                normalize_result(expected_result)
            )

            overall_pass = (
                query_type_pass
                and response_type_pass
                and result_pass
            )

            evaluation_result = {
                "id": test_case["id"],
                "question": question,
                "generated_sql": generated.sql,
                "query_type_pass": query_type_pass,
                "response_type_pass": response_type_pass,
                "result_pass": result_pass,
                "overall_pass": overall_pass
            }

            results.append(
                evaluation_result
            )

            print(
                "Query Type:",
                "PASS" if query_type_pass else "FAIL"
            )

            print(
                "Response Type:",
                "PASS" if response_type_pass else "FAIL"
            )

            print(
                "Database Result:",
                "PASS" if result_pass else "FAIL"
            )

            print(
                "Overall:",
                "PASS" if overall_pass else "FAIL"
            )

            print(
                "Generated SQL:",
                generated.sql
            )

        except Exception as e:

            print(
                "ERROR:",
                str(e)
            )

            results.append({
                "id": test_case["id"],
                "question": question,
                "error": str(e),
                "overall_pass": False
            })

    return results


if __name__ == "__main__":

    # Run evaluation
    results = run_evaluation()

    # Overall Accuracy

    total = len(results)

    passed = sum(
        1
        for result in results
        if result.get("overall_pass")
    )

    accuracy = (
        passed / total * 100
        if total
        else 0
    )

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(f"Total questions: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Overall Accuracy: {accuracy:.2f}%")

    # Component Accuracy

    query_type_passed = sum(
        1
        for result in results
        if result.get(
            "query_type_pass",
            False
        )
    )

    response_type_passed = sum(
        1
        for result in results
        if result.get(
            "response_type_pass",
            False
        )
    )

    result_passed = sum(
        1
        for result in results
        if result.get(
            "result_pass",
            False
        )
    )

    if total > 0:

        print(
            f"Query Type Accuracy: "
            f"{query_type_passed / total * 100:.2f}%"
        )

        print(
            f"Response Type Accuracy: "
            f"{response_type_passed / total * 100:.2f}%"
        )

        print(
            f"Result Accuracy: "
            f"{result_passed / total * 100:.2f}%"
        )

    # Save Evaluation Results

    os.makedirs(
        "evaluation/results",
        exist_ok=True
    )

    with open(
        "evaluation/results/latest_results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            default=str
        )

    print(
        "\nEvaluation report saved to "
        "evaluation/results/latest_results.json"
    )

    