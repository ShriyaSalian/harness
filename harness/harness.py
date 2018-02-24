import src.main.dao.mongo.language_dao as language_dao
import src.main.dao.mongo.component_dao as component_dao
import src.main.dao.mongo.evaluation_dao as evaluation_dao
import src.main.dao.mongo.function_dao as function_dao
import src.main.dao.mongo.parameter_dao as parameter_dao
import src.main.dao.mongo.project_dao as project_dao
import src.main.dao.mongo.statement_dao as statement_dao
import src.main.dao.mongo.workflow_dao as workflow_dao
import src.main.processor.language_processor as language_processor
import src.main.processor.component_processor as component_processor
import src.main.processor.evaluation_processor as evaluation_processor
import src.main.processor.function_processor as function_processor
import src.main.processor.parameter_processor as parameter_processor
import src.main.processor.workflow_processor as workflow_processor


if __name__ == '__main__':
    print('The main harness package. This exposes all the mongo daos and processors.')
