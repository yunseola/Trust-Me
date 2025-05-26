const logoImages = import.meta.glob('@/assets/Bank/*.png', {
  eager: true,
  import: 'default'
});

const logoMap = {};

// 파일명에서 확장자 제거 → 로고 이름으로 매핑
for (const path in logoImages) {
  const fileName = path.split('/').pop().replace('.png', '');
  logoMap[fileName] = logoImages[path];
}

// 전처리 없이, 그대로 은행명으로 접근
export function getBankLogo(name) {
  return logoMap[name] || logoMap['default'];
}
