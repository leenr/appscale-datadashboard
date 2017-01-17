import 'restangular';

export default function create_api_factory(app, config) {
    app.requires.push('restangular');

    return ['Restangular', (Restangular) => {
        return Restangular.withConfig((RestangularProvider) => {
            RestangularProvider.setBaseUrl(config.base_url);
            if(config.response_interceptor) {
                RestangularProvider.addResponseInterceptor(config.response_interceptor);
            }
        })}
    ];
};
