from google.appengine.ext import ndb

from google.appengine.datastore import datastore_query

from .context import ext_context


class QueryIterator(ndb.QueryIterator):
    ''' Version of ndb.query.QueryIterator with support of custom context '''
    def __init__(self, query, options, context=ext_context):
        callback = self._extended_callback
        self._iter = context.iter_query(query, callback=callback, pass_batch_into_callback=True, options=options)
        self._fut = None


@ndb.tasklet
def _run_to_list_async(query, context, results, options=None):
    ''' Version of ndb.query.Query._run_to_list with support of custom context '''

    connection = context._conn

    dsquery = query._get_query(connection)
    rpc = dsquery.run_async(connection, options)

    while rpc is not None:
        batch = yield rpc
        if options and options.offset and batch.skipped_results:
            offset = options.offset - batch.skipped_results
            options = datastore_query.FetchOptions(offset=offset, config=options)

        rpc = batch.next_batch_async(options)
        for result in batch.results:
            result = context._update_cache_from_query_result(result, options)
            if result is not None:
                results.append(result)

    raise ndb.Return(results)


def _make_options(query, q_options):
    if q_options.get('limit', None) is None:
        default_options = query._make_options(q_options)
        if default_options is not None and default_options.limit is not None:
            q_options['limit'] = default_options.limit
        else:
            q_options['limit'] = ndb.query._MAX_LIMIT

    q_options.setdefault('batch_size', q_options['limit'])
    q_options.setdefault('use_cache', False)
    q_options.setdefault('use_memcache', False)

    return query._make_options(q_options)

def do_query(query, context=ext_context, **q_options):
    options = _make_options(query, q_options)

    if query._needs_multi_query():
        return _run_to_list_async(query, context, [], options=options).get_result()
    else:
        # Optimization using direct batches.
        return context.map_query(query, callback=None, options=options)

def do_query_iter(query, context=ext_context, **q_options):
    q_options.setdefault('produce_cursors', True)
    options = _make_options(query, q_options)
    return QueryIterator(query, options)
