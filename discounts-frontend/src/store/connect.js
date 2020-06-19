import axios from 'axios';

async function sendRequest(commit, {
  service,
  url,
  method,
  data,
  headers = {},
  formData = {},
}) {
  try {
    return await axios({
      method,
      url: `${process.env.VUE_APP_BACKEND_URI}/${service}/api/v1${url}`,
      data: data || formData,
      headers,
    });
  } catch (error) {
    const { response } = error;
    if (response.status === 401) {
      commit('security/logout', null, { root: true });
    }
    return response;
  }
}

// eslint-disable-next-line import/prefer-default-export
// eslint-disable-next-line no-return-await
export const postData = async (commit, service, url, data, headers = {}, formData = {}) => await
sendRequest(
  commit, {
    service, url, method: 'POST', data, headers, formData,
  },
);

// eslint-disable-next-line import/prefer-default-export
// eslint-disable-next-line no-return-await
export const getData = async (commit, service, url, data, headers = {}) => await sendRequest(
  commit,
  {
    service, url, method: 'GET', data, headers,
  },
);

// eslint-disable-next-line import/prefer-default-export
// eslint-disable-next-line no-return-await
export const patchData = async (commit, service, url, data, headers = {}) => await sendRequest(
  commit, {
    service, url, method: 'PATCH', data, headers,
  },
);
