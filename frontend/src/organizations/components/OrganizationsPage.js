import React from 'react';
import PropTypes from 'prop-types';

import FontAwesomeIcon from '@fortawesome/react-fontawesome';
import Loading from '../../app/components/Loading';
import ORGANIZATIONS from '../../constants/routes/Organizations';
import OrganizationsTable from './OrganizationsTable';
import * as Routes from '../../constants/routes';
import history from '../../app/History';


const OrganizationsPage = (props) => {
  const { isFetching, items } = props.organizations;
  const isEmpty = items.length === 0;
  return (
    <div className="page_organizations">
      <h1>{props.title}</h1>
      <div className="actions-container">
        <button
          className="btn btn-info"
          type="button"
          onClick={() => (document.location = Routes.BASE_URL + ORGANIZATIONS.EXPORT)}
        >
          <FontAwesomeIcon icon="file-excel" /> Download as .xls
        </button>
        <button
          className="btn btn-info"
          type="button"
          onClick={() => history.push(ORGANIZATIONS.ADD) }
        >
          <FontAwesomeIcon icon="plus" /> Create Organization
        </button>

      </div>
      {isFetching && <Loading />}
      {!isFetching &&
      <OrganizationsTable
        items={items}
        isFetching={isFetching}
        isEmpty={isEmpty}
      />
      }
    </div>
  );
};

OrganizationsPage.propTypes = {
  organizations: PropTypes.shape({
    items: PropTypes.arrayOf(PropTypes.shape()).isRequired,
    isFetching: PropTypes.bool.isRequired
  }).isRequired,
  title: PropTypes.string.isRequired
};

export default OrganizationsPage;
