/*
 * Presentational component
 */
import React from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
import 'react-table/react-table.css';

const Permissions = (props) => {
  const columns = [{
    id: 'name',
    Header: 'Name',
    accessor: item => (item.name)
  }, {
    id: 'description',
    Header: 'Description',
    accessor: item => (item.description)
  }, {
    className: 'col-actions',
    filterable: false,
    Header: '',
    id: 'actions',
    width: 50
  }];

  const filterMethod = (filter, row, column) => {
    const id = filter.pivotId || filter.id;
    return row[id] !== undefined ? String(row[id])
      .toLowerCase()
      .includes(filter.value.toLowerCase()) : true;
  };

  const filterable = true;

  return (
    <ReactTable
      className="searchable"
      data={props.items}
      defaultSorted={[{
        id: 'permission'
      }]}
      filterable={filterable}
      defaultFilterMethod={filterMethod}
      columns={columns}
    />
  );
};

Permissions.propTypes = {
  items: PropTypes.arrayOf(PropTypes.object).isRequired
};

export default Permissions;
