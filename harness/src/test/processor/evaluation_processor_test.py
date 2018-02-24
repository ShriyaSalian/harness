import harness.src.main.processor.evaluation_processor as evaluation_processor


def test_make_evaluations(project, workflow, count=1):
    """Creates the specified number of evaluations, returning them as a collection.
    """
    evaluations = []
    for i in range(0, count):
        evaluations.append(test_make_evaluation(project, workflow))
    return evaluations


def test_get_evaluation_records(project, evaluations):
    evaluation_records = []
    for evaluation in evaluations:
        evaluation_records.append(test_get_evaluation_record(project, evaluation))
    return evaluation_records


def test_get_evaluation_record(project, evaluation):
    """Tests retrieving the associated evaluation record for the given evaluation.
    """
    record = evaluation_processor.get_evaluation_record(project, evaluation)
    return record


def test_make_evaluation(project, workflow):
    """Tests making an evaluation with the given project and workflow.
    """
    evaluation = evaluation_processor.create_evaluation(project, workflow)
    return evaluation


def test_add_evaluation_name(project, workflow, name):
    """Tests adding a name to an evaluation. Returns the updated evaluation.
    """
    recent_evaluations = evaluation_processor.get_evaluations_by_workflow(project, workflow)
    print('Recent evaluation: ')
    print(recent_evaluations[0])
    print('')
    named_evaluation = evaluation_processor.add_evaluation_name(project, recent_evaluations[0], name)
    print('Updated named evaluation: ')
    print(named_evaluation)
    return named_evaluation


if __name__ == '__main__':
    print('Please use evaluation processor test module as test package.')
