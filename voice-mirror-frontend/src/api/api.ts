// create a full file for this to make api calls to my backend using fetch:

import { createLessThan } from "typescript";

const BASE_URL = "http://localhost:8080";

export const fetchApi = async (endpoint: string, method: string, body: any) => {
    const response = await fetch(`${BASE_URL}/${endpoint}/`, {
        method: method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(body),
    });

    if (response.ok) {
        const data = await response.json();
        return { data: data, error: false };
    } else {
        const data = await response.json();
        return { data: data.detail, error: true };
    }
}

export const login = async (username: string, password: string) => {
    return await fetchApi("login", "POST", { username, password });
}

export const signup = async (username: string, password: string) => {
    return await fetchApi("signup", "POST", { username, password });
}

export const chat = async (message: string) => {
    return await fetchApi("chat", "POST", { message })
};

export const persona_create = async (username: string, persona: string, description: string, documents: any[]) => {
    return await  fetchApi("add_persona", "POST", {username, persona, description, documents})
};

export const persona_edit = async (username: string, persona: string, description: string, documents: any[]) => {
    return await  fetchApi("edit_persona", "POST", {username, persona, description, documents})
};