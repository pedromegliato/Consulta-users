import { useCallback, useEffect, useRef, useState } from 'react';

import { fetchUsers } from '../api/usersClient';
import type { FetchUsersResult } from '../domain/user';
import { toUserFacingError } from '../lib/errorMessages';
import type { UserFacingError } from '../lib/errorMessages';

export type FetchUsersState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; result: FetchUsersResult }
  | { status: 'error'; error: UserFacingError };

export function useFetchUsers(onSuccess?: () => void) {
  const [state, setState] = useState<FetchUsersState>({ status: 'idle' });
  const inFlight = useRef<AbortController | null>(null);
  const lastRequest = useRef<number[]>([]);

  useEffect(() => () => inFlight.current?.abort(), []);

  const run = useCallback(
    async (userIds: number[]) => {
      lastRequest.current = userIds;
      inFlight.current?.abort();
      const controller = new AbortController();
      inFlight.current = controller;
      setState({ status: 'loading' });

      try {
        const result = await fetchUsers(userIds, controller.signal);
        setState({ status: 'success', result });
        onSuccess?.();
      } catch (error) {
        if (!controller.signal.aborted) {
          setState({ status: 'error', error: toUserFacingError(error) });
        }
      }
    },
    [onSuccess],
  );

  const retry = useCallback(() => {
    if (lastRequest.current.length > 0) {
      void run(lastRequest.current);
    }
  }, [run]);

  return { state, run, retry };
}
