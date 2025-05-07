import { SSE } from 'sse.js';
import request from "../Service/Request";
import { tokenStore } from 'Service/storeUtil';
import { v4 } from "uuid";
import { getStringEnv } from 'Utils/envUtils';
import { useSystemStore } from '../stores/useSystemStore';

export const runScript = (course_id, lesson_id, input, input_type, script_id, onMessage) => {
  let baseURL  = getStringEnv('baseURL');
  if (baseURL === "" || baseURL === "/") {
    baseURL = window.location.origin;
  }
  const preview_mode = useSystemStore.getState().privewMode;
  const source = new SSE(`${baseURL}/api/study/run?token=${tokenStore.get()}`, {
    headers: { "Content-Type": "application/json", "X-Request-ID": v4().replace(/-/g, '') },
    payload: JSON.stringify({
      course_id, lesson_id, input, input_type, script_id, preview_mode,
    }),
  });
  source.onmessage = (event) => {
    try {
      var response = JSON.parse(event.data);
      if (onMessage) {
        onMessage(response);
      }
    } catch (e) {
    }
  };
  source.onerror = (event) => {
  };
  source.onclose = (event) => {
  };
  source.onopen = (event) => {
  };
  source.close = () => {
  };
  source.stream();
  return source;
};




/**
 * 获取课程学习记录
 * @param {*} lessonId
 * @returns
 */
export const getLessonStudyRecord = async (lessonId) => {
  return request({
    url: "/api/study/get_lesson_study_record?lesson_id=" + lessonId,
    method: "get",
  });
};


export const scriptContentOperation = async (logID, interactionType ) => {
  return request({
    url: '/api/study/script-content-operation',
    method: 'POST',
    data: {
      log_id: logID,
      interaction_type: interactionType
    }
  });
};
