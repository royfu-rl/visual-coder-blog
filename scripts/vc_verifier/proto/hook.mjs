// harness 注入的 three 替身：页面 import 'three' 拿到的是这个模块。
// 它原样导出真 three，只把 WebGLRenderer 换成子类，记下页面最后渲染的 scene / camera / renderer。
// 这样 verifier 能读场景图、换自己的相机重渲，不依赖 agent 主动暴露任何东西。
// 注意 r160 的 render 是构造函数里挂在实例上的，改 prototype 不生效，只能在构造后包一层。
import * as T from '/__vc/three.module.js';
export * from '/__vc/three.module.js';

const vc = (window.__vc = { T, scene: null, camera: null, renderer: null, renders: 0 });

export class WebGLRenderer extends T.WebGLRenderer {
  constructor(opts = {}) {
    super({ ...opts, preserveDrawingBuffer: true });
    const render = this.render;
    this.render = (scene, camera) => {
      if (!vc.busy) Object.assign(vc, { scene, camera, renderer: this, renders: vc.renders + 1 });
      return render.call(this, scene, camera);
    };
  }
}

