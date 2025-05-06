
const USER_TOKEN = 'user_token';

export const setLocalStore = (key: string, value: any = {}) => {
    let localStore: any = window.localStorage;
    if (!localStore) {
        localStore = window.sessionStorage;
    }

    if (value == null || typeof value === 'undefined' || value == '') {
        localStore?.removeItem(key);
    } else {
        localStore?.setItem(key, JSON.stringify(value));
    }
};


export const getLocalStore = (key: string) => {
    let localStore: any = window.localStorage;
    if (!localStore) {
        localStore = window.sessionStorage;
    }

    const value = localStore?.getItem(key);
    try {
        return value ? JSON.parse(value) : undefined;
    } catch {
        return undefined;
    }
};

export const getToken =  () => {
    return getLocalStore(USER_TOKEN) || '';
};

export const setToken = async (token: string) => {
    return setLocalStore(USER_TOKEN, token);
};

export const clearToken = () => {
    return setLocalStore(USER_TOKEN, '');
};
