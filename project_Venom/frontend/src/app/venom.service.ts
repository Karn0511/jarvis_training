
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subject } from 'rxjs';

export interface SystemState {
  status: string;
  detail: string;
  vitals: {
    cpu_percent: number;
    ram_percent: number;
    neural_activity: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class VenomService {
  private socket: WebSocket | null = null;
  public state$ = new Subject<SystemState>();

  constructor(private http: HttpClient) {
    this.connect();
  }

  private connect() {
    // Direct connection to backend (proxy doesn't work reliably for WebSocket)
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//localhost:4200/ws/system-stream`;

    console.log('Connecting to Neural Link:', wsUrl);

    this.socket = new WebSocket(wsUrl);
    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.state$.next(data);
      } catch (e) {
        console.error('Telepathic interference:', e);
      }
    };
    this.socket.onclose = () => {
      console.warn('Neural link severed. reconnecting...');
      setTimeout(() => this.connect(), 2000);
    };
  }

  sendCommand(text: string) {
    // Use relative URL with /api prefix for proxy
    return this.http.post('/api/command', { text });
  }
}
